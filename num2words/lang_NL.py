# -*- encoding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals, print_function
from .lang_EU import Num2Word_EU

class Num2Word_NL(Num2Word_EU):
    def setup(self):
        self.negword = "min"
        self.pointword = "komma"
        self.errmsg_nonnum = u"Maar getalen naar worden kunnen omzetten worden."
        self.errmsg_toobig = u"Word is te groot om in worden te omzetten worden."
        self.exclude_title = ["en", "komma", "min"]
        self.mid_numwords = [(1000, "duizend"), (100, "honderd"),
                             (90, "negentig"), (80, "tachtig"), (70, "zeventig"),
                             (60, "zestig"), (50, "vijftig"), (40, "veertig"),
                             (30, "dertig")]
        self.low_numwords = ["twintig", "negentien", "achtien", "zeventien",
                             "zestien", "vijftien", "veertien", "dertien", "twaalf",
                             "elf", "tien", "negen", "acht", "zeven", "zes",
                             "vijf", "vier", "drie", "twee", "een", "nul"]
        self.ords = {
            "een": "eerste",
            "drie": "derde",
        }

    def set_high_numwords(self, high):
        max = 3 + 6 * len(high)

        for word, n in zip(high, range(max, 3, -6)):
            self.cards[10 ** n] = word + "iljard"
            self.cards[10 ** (n - 3)] = word + "iljoen"

    def splitnum(self, value):
        for elem in self.cards:
            if elem > value:
                continue
            out = []
            if value == 0:
                div, mod = 1, 0
            else:
                div, mod = divmod(value, elem)
            if div == 1 and 100 <= mod < 1000:
                div2, mod2 = divmod(mod, elem/10)
                nb = str(div) + str(div2)
                out.append((self.cards[int(nb)], int(nb)))
                out.append((self.cards[elem / 10], elem / 10))
                if mod2:
                    out.append(self.splitnum(mod2))
            else:
                if div == 1:
                    out.append((self.cards[1], 1))
                else:
                    if div == value:  # The system tallies, eg Roman Numerals
                        return [(div * self.cards[elem], div * elem)]
                    out.append(self.splitnum(div))

                out.append((self.cards[elem], elem))
                if mod:
                    out.append(self.splitnum(mod))
            return out

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next
        if cnum == 1:
            if nnum < 1000000:
                return next
        if nnum < 10 < cnum < 100:
            if ntext[-1:] == 'e':
                ntext, ctext = ctext, ntext + u"ën"
            else:
                ntext, ctext = ctext, ntext + "en"
        elif cnum >= 1010 or nnum >= 10 ** 6:
            ctext += " "
        val = cnum + nnum
        word = ctext + ntext
        return (word, val)

n2w = Num2Word_NL()
to_card = n2w.to_cardinal
to_ord = n2w.to_ordinal
to_ordnum = n2w.to_ordinal_num


def main():
    for val in [1, 11, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 155,
                180, 300, 308, 832, 1000, 1001, 1061, 1100, 1500, 1701, 3000,
                8280, 8291, 150000, 500000, 1000000, 2000000, 2000001,
                -21212121211221211111, -2.121212, -1.0000100]:
        n2w.test(val)

    n2w.test(
        1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730)
    print(n2w.to_currency(112121))
    print(n2w.to_year(1996))


if __name__ == "__main__":
    main()