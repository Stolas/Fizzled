#!/usr/bin/env python
import sys
import logging
from time import sleep
from threading import Thread
import subprocess

logger = logging.getLogger('autopsy')
CRASH_RETURN = 0
NO_CRASH_RETURN = 1

try:
    HAS_VDB = False
    HAS_PYDBG = False
    HAS_CTYPEDBG = False

    # TODO: Add support for windbg / radare ?
    sys.path.append(VDB_ROOT)
    import vtrace
    import vdb
    from envi.archs.i386 import *
    HAS_VDB = True
    logger.debug('Found vivisect.')
except (ImportError, NameError):
    pass #  Failed to load.

try:
    if HAS_VDB:
        raise ImportError('Already found a debugger')

    sys.path.append(PYDBG_ROOT)

    import pydbg  # Reanimate
    HAS_PYDBG = True
    logger.debug('Found pydbg.')
except (ImportError, NameError):
    pass #  Failed to load.

try:
    if HAS_VDB or HAS_PYDBG:
        raise ImportError('Already found a debugger')

    HAS_CTYPEDBG = False # True
    logger.debug('Found ctypes.')
except (ImportError, NameError):
    pass #  Failed to load.


def get_opcode(trace, eip):
    s = trace.readMemory(eip, 15)
    op1 = trace.makeOpcode(s, 0, eip)
    return op1

def load_binary(trace, binary, args):
    execute_path = " ".join([binary] + args)
    logger.debug('Executing {}'.format(execute_path))
    trace.execute(execute_path)
    trace.run()

def print_info(trace):
    # logger.info("META: %s") % (trace.metadata)
    eip = trace.getRegister(REG_EIP)
    es = trace.getRegisterByName("es")
    ds = trace.getRegisterByName("ds")
    cs = trace.getRegisterByName("cs")

    ef = trace.getRegisterByName("eflags")

    edi = trace.getRegister(REG_EDI)
    esi = trace.getRegister(REG_ESI)
    esp = trace.getRegister(REG_ESP)

    logger.info("Bestname: {}".format(trace.getSymByAddr(eip, exact=False)))
    logger.info("%16s: %s" % ("EIP", hex(eip)))

    try:
        dis = get_opcode(trace, trace.getRegister(REG_EIP))
        logger.info("%16s: %s" % ("DIS", dis))
        disLen = len(dis)
        opcode = trace.readMemory(eip, len(dis))
        logger.info("%16s: %s" % ("OPCODE", repr(opcode)))
    except Exception as ex:
        logger.info("%16s: %s" % ("Exception", ex))

    logger.info("%16s: %s" % ("ES", es))
    logger.info("%16s: %s" % ("DS", ds))
    logger.info("%16s: %s" % ("CS", cs))
    logger.info("%16s: %s" % ("EAX", hex(trace.getRegister(REG_EAX))))
    logger.info("%16s: %s" % ("EBX", hex(trace.getRegister(REG_EBX))))
    logger.info("%16s: %s" % ("ECX", hex(trace.getRegister(REG_ECX))))
    logger.info("%16s: %s" % ("EDX", hex(trace.getRegister(REG_EDX))))

    logger.info("%16s: %s" % ("EDI", hex(edi)))
    logger.info("%16s: %s" % ("ESI", hex(esi)))

    logger.info("%16s: %s" % ("ESP", hex(esp)))
    logger.info("%16s: %s" % ("[ESP]", repr(trace.readMemory(esp, 4))))

    logger.info("%16s: %s" % ("Direction", bool(ef & EFLAGS_DF)))


def run_with_vivisect(binary, args, ttl):
    trace = vtrace.getTrace()

    logger.debug('Building Thread [{}]'.format(load_binary))
    t = Thread(target=load_binary, args=(trace, binary, args))
    t.start()
    logger.debug('Sleeping for {} seconds.'.format(ttl))
    sleep(ttl)

    if trace.isRunning():
        trace.sendBreak()
        # print_info(trace)

        logger.info("Death to the process {}".format(trace.getPid()))
        logger.debug("  (\  /)")
        logger.debug(" ( .  .)")
        logger.debug("C(\") (\"), done and no crash. Bunny is sad..")
        trace.kill()
        trace.detach()
        return NO_CRASH_RETURN
    else:
        # TODO: Seems that isRunning isn't working that well.
        logger.info("{} crashed!".format(binary))
        logger.info("Arguments: {}".format(', '.join(args)))
        print_info(trace)
        return CRASH_RETURN

def run_with_pydbg(app, arg, ttl):
    logger.error('Not Implemented pydbg')
    raise NotImplementedError()

def run_with_ctypes(app, arg, ttl):
    logger.error('Nog Implemented ctypes')
    raise NotImplementedError()

def run_simple(app, arg, ttl):
    logger.debug('Starting {} {}'.format(app, arg))
    process = subprocess.Popen([app] + arg)

    sleep(ttl)
    crashed = process.poll()
    if crashed:
        logger.error("Process crashed ({} <- {})".format(app, arg))
        return CRASH_RETURN
    else:
        logger.warning('{} does not crash.'.format(arg))
        process.terminate()
        return NO_CRASH_RETURN

def run(app, arg, ttl, debugger):
    debugger_ok = lambda x: (debugger != None or debugger == x)

    if debugger_ok('vdb'):
        if HAS_VDB:
            return run_with_vivisect(app, arg, ttl)

    elif debugger_ok('pydbg'):
        if HAS_PYDBG:
            return run_with_pydbg(app, arg, ttl)

    elif debugger_ok('ctype'):
        if HAS_CTYPEDBG:
            return run_with_ctypes(app, arg, ttl)
    else:
        if debugger:
            logger.debug('Debugger of choice {} not found, using fallback debugger.'.format(debugger))

    if debugger:
        logger.debug('Required library for {} not found, using fallback debugger.'.format(debugger))

    return run_simple(app, arg, ttl)

if __name__ == '__main__':
    from settings import *
    ret = run(BINARY, ARGUMENTS, TIME_TO_LIVE, DEBUGGER)
    sys.exit(ret)