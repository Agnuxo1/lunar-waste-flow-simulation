# SPDX-FileCopyrightText: 2026 Francisco Angulo de Lafuente
# SPDX-License-Identifier: MIT
# Research-Project: lunar-waste-flow-simulation
# Research-Date: 2026-11-04
# Research-ORCID: https://orcid.org/0009-0001-1634-7063
# Reuse: preserve applicable notices and cite the original author.

"""Mass-flow companion to the Learning from Ants conceptual simulator.

Rates in this model are illustrative. They are not measurements from a lunar system.
"""
import argparse
import json
import math

def simulate(days, initial_organic_kg=1000.0, initial_other_kg=500.0, crew=4):
    """Partition daily feed and recovered outputs, maintaining a mass balance."""
    if type(days) is not int or type(crew) is not int or days < 0 or crew < 0:
        raise ValueError("Use nonnegative whole days and crew size.")
    if not all(math.isfinite(x) and x >= 0 for x in (initial_organic_kg,initial_other_kg)):
        raise ValueError("Use finite, nonnegative initial masses.")
    organic,other=initial_organic_kg,initial_other_kg
    rows=[]
    gas=alcohol=biodiesel=materials=residue=0.
    for day in range(1,days+1):
        organic+=1.5*crew
        other+=1.0*crew
        feed=organic*.1
        inorganic=other*.1
        organic-=feed
        other-=inorganic
        gas+=.3*feed
        alcohol+=.2*feed
        biodiesel+=.1*feed
        residue+=.4*feed
        materials+=inorganic
        total=organic+other+gas+alcohol+biodiesel+residue+materials
        expected=initial_organic_kg+initial_other_kg+day*2.5*crew
        if not math.isclose(total,expected,rel_tol=1e-12,abs_tol=1e-9):
            raise ArithmeticError("Mass balance violated.")
        rows.append(dict(day=day,organic_kg=organic,other_kg=other,
                         recovered_kg=gas+alcohol+biodiesel+materials,residue_kg=residue,total_kg=total))
    return rows

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days",type=int,default=14)
    parser.add_argument("--crew",type=int,default=4)
    args=parser.parse_args()
    print(json.dumps(simulate(args.days,crew=args.crew),indent=2))

if __name__=="__main__":
    main()
