"""
"""
from csvw.dsv import UnicodeWriter
from pygrambank.cli_util import add_wiki_repos

SHEETS = """\
MD-GR-RSI_kand1301
CB-PE-AS_sout2969
CB-PE-AS_utee1244
CB-PE-AS_chem1251
CB-PE-AS_wanm1242
CB-PE-AS_biri1256
CB-PE-AS_east2379
CB-PE-AS_naru1238
CB-PE-AS_pany1241
CB-PE-AS_pint1250
CB-PE-AS_yagu1244
CB-PE-AS_pemo1248
CB-PE-AS_thur1254
CB-PE-AS_woiw1237
CB-PE-AS_coca1259
CB-PE-AS_macu1260
CB-PE-AS_muru1266
CB-PE-AS_nyul1247
CB-PE-AS_para1316
CB-PE-AS_sanu1240
CB-PE-AS_tuca1252
CB-PE-AS_cacu1241
CB-PE-AS_djin1253
CB-PE-AS_guan1269
CB-PE-AS_guny1241
CB-PE-AS_kari1311
CB-PE-AS_mats1244
CB-PE-AS_wira1262
CB-PE-AS_wira1265
CB-PE-AS_yala1262
CB-PE-AS_daww1239
CB-PE-AS_aghu1254
CB-PE-AS_bora1263
CB-PE-AS_dhar1247
CB-PE-AS_dyir1250
CB-PE-AS_kore1283
CB-PE-AS_wath1238
CB-PE-AS_arab1267
CB-PE-AS_duun1241
CB-PE-AS_nina1238
CB-PE-AS_walm1241
CB-PE-AS_yano1262
CB-PE-AS_guah1255
CB-PE-AS_cube1242
CB-PE-AS_darl1243
CB-PE-AS_desa1247
CB-PE-AS_inga1252
CB-PE-AS_kain1272
CB-PE-AS_macu1259
CB-PE-AS_mapu1245
CB-PE-AS_maqu1238
CB-PE-AS_sion1247
CB-PE-AS_warr1255
CB-PE-AS_ying1247
CB-PE-AS_bara1380
CB-PE-AS_awab1243
CB-PE-AS_dier1241
CB-PE-AS_kara1476
CB-PE-AS_nant1250
CB-PE-AS_kaur1267
CB-PE-AS_nyan1301
CB-PE-AS_waru1264
CB-PE-AS_yand1253
CB-PE-AS_yort1237
CB-PE-AS_nort2954
CB-PE-AS_kawa1283
CB-PE-AS_pana1305
CB-PE-AS_cupe1243
HS_wann1242
MD-GR-RSI_unaa1239
CB-PE-AS_wang1291"""


def register(parser):
    add_wiki_repos(parser)


def add_col(sheet, features):
    rows = list(sheet.iterrows())
    if 'Feature' in rows[0]:
        return False
    with UnicodeWriter(sheet.path, delimiter='\t', encoding='utf8') as w:
        for i, row in enumerate(rows):
            if i == 0:
                w.writerow(['Feature'] + list(row.keys()))
            w.writerow([features.get(row['Feature_ID'], '')] + list(row.values()))
    return True


def run(args):  # pragma: no cover
    features = {f.id: f.wiki['title'] for f in args.repos.features.values()}
    for sheet in args.repos.iter_sheets():
        if sheet.path.stem in SHEETS:
            if add_col(sheet, features):
                args.log.info('{} written'.format(sheet.path))
