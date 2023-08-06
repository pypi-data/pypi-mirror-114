from __future__ import annotations
from string import Template
from functools import lru_cache
from typing import List, Dict, Any
import re

# In all templates we make the difference between substitutions which
# are constant (with the form ${subst} and substitutions which respond
# to the configuration of a specific engine / offline renderer ({subst})

_orc = r"""
sr     = ${sr}
ksmps  = ${ksmps}
nchnls = ${nchnls}
; nchnls_i = ${nchnls_i}
0dbfs  = 1
A4     = ${a4}

${includes}

gi__responses       ftgen  ${responses}, 0, ${numtokens}, -2, 0
gi__subgains        ftgen  ${subgains},  0, 100, -2, 0
gi__tokenToInstrnum ftgen ${tokenToInstrnum}, 0, ${maxNumInstrs}, -2, 0

${globalcode}

; ---------------------------------
;          builtin-instruments
; ---------------------------------


instr __init
    
    ; ftset gi__subgains, 1 
    
endin





schedule "__init", 0, 1

"""

_busOrc = r'''

#define _BUSUNSET #${BUSUNSET}#

; The actual buses
ga__buses[]   init ${numAudioBuses}
gi__bustable ftgen 0, 0, ${numControlBuses}, -2, 0
; gk__buses[]   init ${numControlBuses}

; This table keeps track of the number of references a bus has
gi__busrefs ftgen 0, 0, ${numAudioBuses}, -2, 0
gi__busrefsk ftgen 0, 0, ${numControlBuses}, -2, 0

; A pool of bus indexes
gi__buspool pool_gen ${numAudioBuses}
gi__buspoolk pool_gen ${numControlBuses} 

; A dict mapping bustoken to bus number
gi__bustoken2num dict_new "int:float"
gi__bustoken2numk dict_new "int:float"

chn_k "_busTokenCount", 3

instr __businit
    chnset 0, "_busTokenCount"
    ftset gi__bustable, $$_BUSUNSET
    turnoff
endin

instr ${clearbuses}
    zeroarray ga__buses
endin

opcode busassign, i, io
    itoken, ikind xin
    if itoken == -1 then
        itoken chnget "_busTokenCount"
    endif
    if ikind == 0 then
        ibus pool_pop gi__buspool, -1
    else
        ibus pool_pop gi__buspoolk, -1
    endif
    
    if ibus == -1 then
        initerror "busassign failed, out of buses"
    endif
    
    dict_set gi__bustoken2num, itoken, ibus
    chnset itoken+1, "_busTokenCount"
    xout ibus
endop

instr _busassign
    itoken = p4
    ikind = p5
    ibus busassign itoken, ikind
endin

instr _busrelease  ; release audio bus
    itoken = p4
    ibus dict_get gi__bustoken2num, itoken, -99999999
    if ibus == -99999999 then
        initerror sprintf("itoken %d has no bus assigned to it", itoken)
    endif
    
    irefs tab_i ibus, gi__busrefs
    if irefs <= 1 then
        if pool_isfull:i(gi__buspool) == 1 then
            initerror "Bus pool is full!"
        endif
        pool_push gi__buspool, ibus
        dict_del gi__bustoken2num, itoken
        tabw_i 0, ibus, gi__busrefs
    else   
        tabw_i irefs-1, ibus, gi__busrefs
    endif
endin

instr _busreleasek
    itoken = p4
    ibus dict_get gi__bustoken2num, itoken, -99999999
    if ibus == -99999999 then
        initerror sprintf("itoken %d has no bus assigned to it", itoken)
    endif
    irefs tab_i ibus, gi__busrefsk
    if irefs <= 1 then
        if pool_isfull:i(gi__buspoolk) == 1 then
            initerror "Bus pool is full!"
        endif
        pool_push gi__buspoolk, ibus
        dict_del gi__bustoken2num, itoken
        tabw_i 0, ibus, gi__busrefsk
        ; gk__buses[ibus] = $$_BUSUNSET
        tabw_i $$_BUSUNSET, ibus, gi__bustable
    else   
        tabw_i irefs-1, ibus, gi__busrefsk
    endif
endin

opcode _bususe, i, i
    itoken xin
    ibus dict_get gi__bustoken2num, itoken, -1
    if ibus == -1 then
        ibus = busassign(itoken)
    endif
    irefs tab_i ibus, gi__busrefs
    tabw_i irefs+1, ibus, gi__busrefs
    atstop "_busrelease", 0, 0, itoken
    xout ibus
endop

instr _busaddref
    itoken = p4
    ibus dict_get gi__bustoken2num, itoken, -1
    if ibus == -1 then
        ibus = busassign(itoken)
    endif
    irefs tab_i ibus, gi__busrefs
    tabw_i irefs+1, ibus, gi__busrefs
endin

opcode _bususek, i, i
    itoken xin
    ibus dict_get gi__bustoken2num, itoken, -9999999
    if ibus == -9999999 then
        ibus = busassign(itoken, 1)
    endif
    irefs tab_i ibus, gi__busrefsk
    tabw_i irefs+1, ibus, gi__busrefsk
    atstop "_busreleasek", 0, 0, itoken
    xout ibus
endop

opcode _busget, i, ii
    itoken, ikind xin
    ibus dict_get gi__bustoken2num, itoken, -9999999
    if ibus == -9999999 then
        ibus = busassign(itoken, ikind)
        prints "Assigning k-bus %d to token %d\n", ibus, itoken
    endif
    xout ibus
endop

instr _busindex
    isynctoken = p4
    ibustoken = p5
    iassign = p6
    ibus dict_get gi__bustoken2num, ibustoken, -1
    if ibus == -1 && iassign == 1 then
        ibus = busassign(ibustoken, 1)
    endif
    tabw_i ibus, isynctoken, gi__responses
    outvalue "__sync__", isynctoken
endin

opcode busin, a, i
    itoken xin
    ibus = _bususe(itoken)
    xout ga__buses[ibus]
endop

opcode busin, k, io
    itoken, idefault xin
    ibus = _bususek(itoken)
    prints "busin: %d, ibus: %d\n", itoken, ibus
    ; init
    ival tab_i ibus, gi__bustable
    print ival
    if ival == $$_BUSUNSET then
        prints "bus %d unset, setting to default %f\n", ibus, idefault
        tabw_i idefault, ibus, gi__bustable
    endif
    
    kval tab ibus, gi__bustable
    xout kval
endop

opcode busout, 0, ia
    itoken, asig xin
    ibus = _bususe(itoken)
    ga__buses[ibus] = asig
endop

opcode busout, 0, ik
    itoken, ksig xin
    ibus = _bususek(itoken)
    ; gk__buses[ibus] = ksig
    tabw ksig, ibus, gi__bustable
endop

opcode busout, 0, ii
    itoken, isig xin
    ibus = _busget(itoken, 1)
    ; gk__buses[ibus] = isig
    tabw_i isig, ibus, gi__bustable
endop

opcode busmix, 0, ia
    itoken, asig xin
    ibus = _bususe(itoken)
    ga__buses[ibus] = ga__buses[ibus] + asig
endop

instr _busoutk
    itoken = p4
    ivalue = p5
    ibus = _busget(itoken, 1)
    ; gk__buses[ibus] = ivalue
    tabw_i ivalue, ibus, gi__bustable
endin

schedule "__businit", 0, ksmps/sr
'''


def _extractInstrNames(s:str) -> List[str]:
    names = []
    for line in s.splitlines():
        if match := re.search(r"\binstr\s+\$\{(\w+)\}", line):
            instrname = match.group(1)
            names.append(instrname)
    return names


_instrNames = _extractInstrNames(_orc)

# Constants
CONSTS = {
    'numtokens': 1000,
    'eventMaxSize': 1999,
    'highestInstrnum': 11500,
    'postProcInstrnum': 11000,
    'reservedTablesStart': 300,
    'reservedInstrsStart': 500,
    'numReservedTables': 2000,
    'maxNumInstrs': 10000,
    'BUSUNSET': -999999999
}

_tableNames = ['responses', 'subgains', 'tokenToInstrnum']

BUILTIN_INSTRS = {k:i for i, k in enumerate(_instrNames, start=CONSTS['reservedInstrsStart'])}
BUILTIN_INSTRS['clearbuses'] = CONSTS['postProcInstrnum']
BUILTIN_TABLES = {name:i for i, name in enumerate(_tableNames, start=1)}


@lru_cache(maxsize=0)
def orcTemplate(busSupport=True) -> Template:
    parts = [_orc]
    if busSupport:
        parts.append(_busOrc)
    orc = "\n".join(parts)
    return Template(orc)


def makeOrc(sr:int, ksmps:int, nchnls:int, nchnls_i:int,
            backend:str, a4:float, globalcode:str="", includestr:str="",
            numAudioBuses:int=32,
            numControlBuses:int=64):
    withBusSupport = numAudioBuses > 0 or numControlBuses > 0
    withBusSupport = False
    template = orcTemplate(busSupport=withBusSupport)
    subs: Dict[str, Any] = {name:f"{num} ; {name}"
                            for name, num in BUILTIN_INSTRS.items()}
    subs.update(BUILTIN_TABLES)
    subs.update(CONSTS)
    orc = template.substitute(
            sr=sr,
            ksmps=ksmps,
            nchnls=nchnls,
            nchnls_i=nchnls_i,
            backend=backend,
            a4=a4,
            globalcode=globalcode,
            includes=includestr,
            numAudioBuses=numAudioBuses,
            numControlBuses=numControlBuses,
            **subs
    )
    return orc

def busSupportCode(numAudioBuses:int,
                   clearBusesInstrnum:int,
                   numControlBuses:int) -> str:
    return Template(_busOrc).substitute(numAudioBuses=numAudioBuses,
                                        clearbuses=f'{clearBusesInstrnum} ;  clearbuses',
                                        numControlBuses=numControlBuses,
                                        BUSUNSET=CONSTS['BUSUNSET'])
