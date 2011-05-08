import MySQLdb
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.encoding import smart_unicode, smart_str
from node.models import Entry



class Command(BaseCommand):
    def handle(self, *args, **options):

        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="t", charset = "utf8", use_unicode = True)
        cur = db.cursor()
        cur.execute("""SELECT
                drp_node.nid, drp_node.type, drp_node.title, drp_node.created, drp_node_revisions.body
            FROM drp_node JOIN drp_node_revisions ON drp_node.nid=drp_node_revisions.nid""")

        for row in cur.fetchall():
            tag_cur = db.cursor()
            tag_cur.execute("""SELECT drp_term_data.name FROM drp_term_node JOIN drp_term_data ON drp_term_data.tid=drp_term_node.tid WHERE drp_term_node.nid = {0}""".format(row[0]))

            tags_list = []
            for tag in tag_cur.fetchall():
                tag = smart_unicode(tag[0])
                if not tag.upper() == tag:
                    tag = tag.title()
                tags_list.append(tag)

            tags = ",".join(tags_list)

            Entry.objects.create(
                nid=row[0],
                title=row[2],
                slug="",
                body=row[4],
                coments=1,
                is_page=1 if row[1]=="page" else 0,
                page_url="",
                created=datetime.fromtimestamp(row[3]),
                edited=row[3],
                tags=tags,
            )

        print "OK"