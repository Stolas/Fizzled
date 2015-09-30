#!/usr/bin/env python
import sys
import logging
from time import sleep
from threading import Thread
import subprocess
from settings import *

logger = logging.getLogger('autopsy')

try:
    # TODO: Add support for windbg / radare ?
    sys.path.append(VDB_ROOT)
    import vtrace
    import vdb
    from envi.archs.i386 import *
    HAS_VDB = True
    logger.debug('Vivisect found.')
except (ImportError, NameError):
    HAS_VDB = False
    logger.debug('Vivisect NOT found.')



def get_opcode(trace, eip):
    s = trace.readMemory(eip, 15)
    op1 = trace.makeOpcode(s, 0, eip)
    return op1

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
        print_info(trace)

        logger.info("Death to the process {}".format(trace.getPid()))
        logger.debug("  (\  /)")
        logger.debug(" ( .  .)")
        logger.debug("C(\") (\"), done and no crash. Bunny is sad..")
        trace.kill()
        trace.detach()
        sys.exit(0)
    else:
        # TODO: Seems that isRunning isn't working that well.
        logger.info("{} crashed!".format(binary))
        logger.info("Arguments: {}".format(', '.join(args)))
        print_info(trace)
        sys.exit(1)


def run_simple(app, arg, ttl):
    logger.debug('Starting {} {}'.format(app, arg))
    process = subprocess.Popen([app] + arg)

    sleep(ttl)
    crashed = process.poll()
    if crashed:
        logger.error("Process crashed ({} <- {})".format(app, arg))
        sys.exit(0)
    else:
        process.terminate()
        sys.exit(1)


def load_binary(trace, binary, args):
    execute_path = " ".join([binary] + args)
    logger.debug('Executing {}'.format(execute_path))
    trace.execute(execute_path)
    trace.run()


if __name__ == '__main__':
    run = run_simple
    if HAS_VDB:
        run = run_with_vivisect
    run(BINARY, ARGUMENTS, TIME_TO_LIVE)
