from DZDutils.neo4j import run_periodic_iterate
import py2neo

delete_pmids = []

run_periodic_iterate(
    graph=py2neo.Graph(),
    cypherIterate="UNWIND $pmids as pm_id return pm_id",
    cypherAction="MERGE (n:PubmedArticle{PMID:pm_id}) SET n:_PubmedArticle_DELETED",
    parallel=True,
    params={"pmids": delete_pmids},
)
