from datetime import date
import atomium
from unittest import TestCase

class MmcifFileDictReadingTests(TestCase):

    def test_1lol_file_dict(self):
        d = atomium.open("tests/integration/files/1lol.cif", file_dict=True)
        self.assertEqual(d["entry"], [{"id": "1LOL"}])
        self.assertEqual(d["audit_author"], [
         {"name": "Wu, N.", "pdbx_ordinal": "1"},
         {"name": "Pai, E.F.", "pdbx_ordinal": "2"}
        ])
        self.assertEqual(d["struct"][0]["title"][:7], "Crystal")
        entity = d["entity"]
        self.assertEqual(len(entity), 4)
        self.assertEqual(
         entity[0]["pdbx_description"], "orotidine 5'-monophosphate decarboxylase"
        )
        self.assertTrue(
         d["entity_poly"][0]["pdbx_seq_one_letter_code"].startswith("LRSRRVDVM")
        )
        self.assertTrue(
         d["entity_poly"][0]["pdbx_seq_one_letter_code"].endswith("IESIKDLLIPE")
        )
        self.assertEqual(entity[1]["type"], "non-polymer")
        self.assertTrue(d["citation"][0]["title"].startswith("Crystal"))
        self.assertTrue(d["citation"][0]["title"].endswith("decarboxylase."))



class MmtfFileDictReadingTests(TestCase):

    def test_1lol_file_dict(self):
        d = atomium.open("tests/integration/files/1lol.mmtf", file_dict=True)
        self.assertEqual(d["mmtfVersion"], "1.0.0")
        self.assertEqual(len(d["unitCell"]), 6)
        self.assertAlmostEqual(d["unitCell"][0], 57.57, delta=0.00005)
        self.assertAlmostEqual(d["resolution"], 1.9, delta=0.00005)
        self.assertEqual(d["numAtoms"], 3431)
        self.assertEqual(len(d["secStructList"]), 602)
        self.assertEqual(d["secStructList"][:5], (7, 4, 4, 4, 3))
        self.assertEqual(len(d["bondAtomList"]), 828)
        self.assertEqual(d["bondAtomList"][:6], (7, 2, 15, 9, 23, 17))
        self.assertEqual(d["chainIdList"], list("ABCDEFGH"))
        self.assertEqual(d["insCodeList"], [""] * 602)
        self.assertEqual(d["sequenceIndexList"][:6], [10, 11, 12, 13, 14, 15])
        self.assertEqual(d["occupancyList"], [1.0] * 3431)
        self.assertEqual(d["xCoordList"][:3], [3.696, 3.198, 3.914])
        self.assertEqual(d["bFactorList"][:3], [21.5, 19.76, 19.29])
        self.assertEqual(d["groupList"][0]["groupName"], "ASN")
        self.assertEqual(d["groupList"][0]["atomNameList"][:3], ["N", "CA", "C"])


    def test_1igt_file_dict(self):
        d = atomium.open("tests/integration/files/1igt.mmtf", file_dict=True)
        self.assertEqual(d["mmtfVersion"], "1.0.0")
        self.assertEqual(d["insCodeList"][266], "A")



class PdbFileDictReadingTests(TestCase):

    def test_1lol_file_dict(self):
        d = atomium.open("tests/integration/files/1lol.pdb", file_dict=True)
        self.assertEqual(d["HEADER"], [
         "HEADER    LYASE                                   06-MAY-02   1LOL"
        ])
        self.assertEqual(d["HETNAM"], [
         "HETNAM     BU2 1,3-BUTANEDIOL", "HETNAM     XMP XANTHOSINE-5'-MONOPHOSPHATE"
        ])
        self.assertEqual(d["CONECT"][0], "CONECT 3194 3195 3196")
        self.assertEqual(len(d["REMARK"].keys()), 16)
        self.assertEqual(d["REMARK"]["2"][1], "REMARK   2 RESOLUTION.    1.90 ANGSTROMS.")
        self.assertEqual(len(d["MODEL"]), 1)
        self.assertEqual(len(d["MODEL"][0]), 3433)
        self.assertEqual(
         d["MODEL"][0][0],
         "ATOM      1  N   VAL A  11       3.696  33.898  63.219  1.00 21.50           N"
        )


    def test_5xme_file_dict(self):
        d = atomium.open("tests/integration/files/5xme.pdb", file_dict=True)
        self.assertEqual(d["HEADER"], [
         "HEADER    APOPTOSIS                               15-MAY-17   5XME"
        ])
        self.assertEqual(len(d["MODEL"]), 10)
        self.assertEqual(len(d["MODEL"][0]), 1828)
        self.assertEqual(
         d["MODEL"][1][4],
         "ATOM      5  CB  ALA A 199      36.093  -8.556  -1.452  1.00  0.00           C"
        )



class DataDictReadingTests(TestCase):

    def test_1lol_data_dict(self):
        for f in ["cif", "mmtf", "pdb"]:
            d = atomium.open("tests/integration/files/1lol." + f, data_dict=True)
            self.assertEqual(set(d.keys()), {
             "description", "experiment", "quality", "geometry", "models"
            })
            if f == "pdb":
                self.assertEqual(d["description"], {
                 "code": "1LOL",
                 "title": "CRYSTAL STRUCTURE OF OROTIDINE MONOPHOSPHATE DECARBOXYLASE COMPLEX WITH XMP",
                 "deposition_date": date(2002, 5, 6),
                 "classification": "LYASE",
                 "keywords": ["TIM BARREL", "LYASE"],
                 "authors": ["N.WU", "E.F.PAI"]
                })
            else:
                self.assertEqual(d["description"], {
                 "code": "1LOL",
                 "title": "Crystal structure of orotidine monophosphate decarboxylase complex with XMP",
                 "deposition_date": date(2002, 5, 6),
                 "classification": None if f == "mmtf" else "LYASE",
                 "keywords": [] if f == "mmtf" else ["TIM barrel", "LYASE"],
                 "authors": [] if f == "mmtf" else ["Wu, N.", "Pai, E.F."]
                })
            if f == "pdb":
                self.assertEqual(d["experiment"], {
                 "technique": "X-RAY DIFFRACTION",
                 "source_organism": "METHANOTHERMOBACTER THERMAUTOTROPHICUS STR. DELTA H",
                 "expression_system": "ESCHERICHIA COLI"
                })
            else:
                self.assertEqual(d["experiment"], {
                 "technique": "X-RAY DIFFRACTION",
                 "source_organism": None if f == "mmtf" else "Methanothermobacter thermautotrophicus str. Delta H",
                 "expression_system": None if f == "mmtf" else "Escherichia coli"
                })
            self.assertEqual(d["quality"], {
             "resolution": 1.9, "rvalue": 0.193, "rfree": 0.229
            })
            self.assertEqual(d["geometry"], {"assemblies": [{
             "id": 1,
             "software": None if f == "mmtf" else "PISA",
             "delta_energy": None if f == "mmtf" else -31.0,
             "buried_surface_area": None if f == "mmtf" else 5230,
             "surface_area": None if f == "mmtf" else 16550,
             "transformations": [{
              "chains": ["A", "B"] if f == "pdb" else ["A", "B", "C", "D", "E", "F", "G", "H"],
              "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
              "vector": [0.0, 0.0, 0.0]
             }]
            }]})
            self.assertEqual(len(d["models"]), 1)
            self.assertEqual(len(d["models"][0]["polymer"]), 2)
            self.assertEqual(len(d["models"][0]["polymer"]["A"]["sequence"]), 229)
            self.assertEqual(len(d["models"][0]["polymer"]["A"]["residues"]), 204)
            self.assertEqual(d["models"][0]["polymer"]["A"]["sequence"][:2], "LR")
            self.assertEqual(len(d["models"][0]["polymer"]["A"]["residues"]["A.11"]["atoms"]), 7)
            self.assertEqual(d["models"][0]["polymer"]["A"]["residues"]["A.11"]["atoms"][1], {
             "element": "N", "name": "N", "x": 3.696, "y": 33.898, "z": 63.219,
             "bvalue": 21.5, "charge": 0.0, "occupancy": 1.0, "alt_loc": None,
             "anisotropy": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            })
            self.assertEqual(d["models"][0]["polymer"]["A"]["residues"]["A.11"]["name"], "VAL")
            self.assertEqual(d["models"][0]["polymer"]["B"]["residues"]["B.1011"]["atoms"][1558 + (f == "pdb")], {
             "element": "N", "name": "N", "x": -26.384, "y": 61.433, "z": 36.898,
             "bvalue": 39.3, "charge": 0.0, "occupancy": 1.0, "alt_loc": None,
             "anisotropy": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            })
            self.assertEqual(len(d["models"][0]["non-polymer"]), 4)
            self.assertEqual(d["models"][0]["non-polymer"]["A.5001"]["name"], "BU2")
            self.assertEqual(d["models"][0]["non-polymer"]["A.5001"]["internal_id"], "A" if f == "pdb" else "C")
            self.assertEqual(len(d["models"][0]["non-polymer"]["A.5001"]["atoms"]), 6)
            self.assertEqual(d["models"][0]["non-polymer"]["A.5001"]["polymer"], "A")
            self.assertEqual(d["models"][0]["non-polymer"]["B.2002"]["name"], "XMP")
            self.assertEqual(d["models"][0]["non-polymer"]["B.2002"]["internal_id"], "B" if f == "pdb" else "F")
            self.assertEqual(len(d["models"][0]["non-polymer"]["B.2002"]["atoms"]), 24)
            self.assertEqual(d["models"][0]["non-polymer"]["B.2002"]["polymer"], "B")
            self.assertEqual(len(d["models"][0]["water"]), 180)
            self.assertEqual(d["models"][0]["water"]["A.3005"]["name"], "HOH")
            self.assertEqual(d["models"][0]["water"]["A.3005"]["internal_id"], "A" if f == "pdb" else "G")
            self.assertEqual(d["models"][0]["water"]["A.3005"]["polymer"], "A")
            self.assertEqual(d["models"][0]["water"]["B.3180"]["name"], "HOH")
            self.assertEqual(d["models"][0]["water"]["B.3180"]["internal_id"], "B" if f == "pdb" else "H")
            self.assertEqual(d["models"][0]["water"]["B.3180"]["polymer"], "B")


    def test_1xda_data_dict(self):
        for f in ["cif", "mmtf", "pdb"]:
            d = atomium.open("tests/integration/files/1xda." + f, data_dict=True)
            self.assertEqual(len(d["geometry"]["assemblies"]), 12)
            self.assertEqual(d["geometry"]["assemblies"][0], {
             "id": 1,
             "software": None if f == "mmtf" else "PISA",
             "delta_energy": None if f == "mmtf" else -7.0,
             "buried_surface_area": None if f == "mmtf" else 1720.0,
             "surface_area": None if f == "mmtf" else 3980.0,
             "transformations": [{
              "chains": ["A", "B"] if f == "pdb" else ["A", "B", "I", "J", "K", "L", "Y", "Z"],
              "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
              "vector": [0.0, 0.0, 0.0]
             }]
            })
            if f == "pdb":
                self.assertEqual(d["geometry"]["assemblies"][4], {
                 "id": 5,
                 "software": "PISA",
                 "delta_energy": -332.0,
                 "buried_surface_area": 21680.0,
                 "surface_area": 12240.0,
                 "transformations": [{
                  "chains": ["E", "F", "G", "H"],
                  "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
                  "vector": [0.0, 0.0, 0.0]
                 }, {
                  "chains": ["E", "F", "G", "H"],
                  "matrix": [[-0.5, -0.866025, 0.0], [0.866025, -0.5, 0.0], [0.0, 0.0, 1.0]],
                  "vector": [0.0, 0.0, 0.0]
                 }, {
                  "chains": ["E", "F", "G", "H"],
                  "matrix": [[-0.5, 0.866025, 0.0], [-0.866025, -0.5, 0.0], [0.0, 0.0, 1.0]],
                  "vector": [0.0, 0.0, 0.0]
                 }]
                })
            else:
                self.assertEqual(d["geometry"]["assemblies"][4], {
                 "id": 5,
                 "software": None if f == "mmtf" else "PISA",
                 "delta_energy": None if f == "mmtf" else -332.0,
                 "buried_surface_area": None if f == "mmtf" else 21680.0,
                 "surface_area": None if f == "mmtf" else 12240.0,
                 "transformations": [{
                  "chains": ["E", "F", "G", "H", "Q", "R", "S", "T", "U", "V", "W", "X", "CA", "DA", "EA", "FA"],
                  "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
                  "vector": [0.0, 0.0, 0.0]
                 }, {
                  "chains": ["E", "F", "G", "H", "Q", "R", "S", "T", "U", "V", "W", "X", "CA", "DA", "EA", "FA"],
                  "matrix": [[-0.5, -0.8660254038, 0.0], [0.8660254038, -0.5, 0.0], [0.0, 0.0, 1.0]],
                  "vector": [0.0, 0.0, 0.0]
                 }, {
                  "chains": ["E", "F", "G", "H", "Q", "R", "S", "T", "U", "V", "W", "X", "CA", "DA", "EA", "FA"],
                  "matrix": [[-0.5, 0.8660254038, 0.0], [-0.8660254038, -0.5, 0.0], [0.0, 0.0, 1.0]],
                  "vector": [0.0, 0.0, 0.0]
                 }]
                })


    def test_1m4x_data_dict(self):
        for f in ["cif", "mmtf", "pdb"]:
            d = atomium.open("tests/integration/files/1m4x." + f, data_dict=True)
            self.assertEqual(len(d["geometry"]["assemblies"]), 1 if f == "pdb" else 7)
            self.assertEqual(len(d["geometry"]["assemblies"][0]["transformations"]), 1680)
            if f != "pdb":
                self.assertEqual(len(d["geometry"]["assemblies"][2]["transformations"]), 140)
                self.assertEqual(len(d["geometry"]["assemblies"][3]["transformations"]), 168)
                self.assertEqual(len(d["geometry"]["assemblies"][4]["transformations"]), 30)
                self.assertEqual(len(d["geometry"]["assemblies"][5]["transformations"]), 66)
            self.assertEqual(
             d["geometry"]["assemblies"][0]["transformations"][29]["chains"],
             ["A", "B", "C"]
            )
            self.assertAlmostEqual(
             d["geometry"]["assemblies"][0]["transformations"][29]["vector"][0],
             -18.95, delta=0.005
            )
            self.assertAlmostEqual(
             d["geometry"]["assemblies"][0]["transformations"][29]["matrix"][0][0],
             0.812, delta=0.005
            )
            self.assertAlmostEqual(
             d["geometry"]["assemblies"][0]["transformations"][29]["matrix"][-1][-1],
             0.286, delta=0.005
            )


    def test_5xme_data_dict(self):
        for f in ["cif", "mmtf", "pdb"]:
            d = atomium.open("tests/integration/files/5xme." + f, data_dict=True)
            self.assertEqual(d["experiment"]["technique"], "SOLUTION NMR")
            self.assertEqual(d["quality"], {
             "resolution": None, "rvalue": None, "rfree": None
            })
            self.assertEqual(len(d["models"]), 10)
            for model in d["models"][1:]:
                self.assertEqual(len(model["polymer"]), len(d["models"][0]["polymer"]))
                self.assertEqual(len(model["non-polymer"]), len(d["models"][0]["non-polymer"]))
                self.assertEqual(len(model["water"]), len(d["models"][0]["water"]))
            self.assertEqual(d["models"][0]["polymer"]["A"]["residues"]["A.199"]["atoms"][1]["x"], 33.969)
            self.assertEqual(d["models"][1]["polymer"]["A"]["residues"]["A.199"]["atoms"][1 if f == "pdb" else 1828]["x"], 34.064)


    def test_4y60_data_dict(self):
        for f in ["cif", "mmtf", "pdb"]:
            d = atomium.open("tests/integration/files/4y60.cif", data_dict=True)
            self.assertEqual(d["models"][0]["polymer"]["A"]["sequence"][:2], "CA")
            if f != "mmtf":
                self.assertEqual(d["models"][0]["polymer"]["C"]["residues"]["C.0"]["atoms"][1], {
                 "element": "N", "name": "N", "x": 43.447, "y": -56.622, "z": -20.561,
                 "bvalue": 56.53, "charge": 0.0, "occupancy": 1.0, "alt_loc": None,
                 "anisotropy": [0.9838, 0.7489, 0.4152, -0.1159, -0.0115, -0.2655],
                })


    def test_1cbn_data_dict(self):
        for f in ["cif", "mmtf", "pdb"]:
            d = atomium.open("tests/integration/files/1cbn.cif", data_dict=True)
            self.assertEqual(d["models"][0]["polymer"]["A"]["residues"]["A.1"]["atoms"][1], {
             "element": "N", "name": "N", "x": 16.864, "y": 14.059, "z": 3.442,
             "bvalue": 6.22, "charge": 0.0, "occupancy": 0.8, "alt_loc": "A",
             "anisotropy": [0, 0, 0, 0, 0, 0],
            })
