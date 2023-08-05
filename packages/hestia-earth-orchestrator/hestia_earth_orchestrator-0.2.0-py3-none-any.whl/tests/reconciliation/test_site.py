from unittest.mock import patch
import json
import os
from tests.utils import overwrite_results, fixtures_path, order_lists

from hestia_earth.orchestrator import run

site_path = os.path.join(fixtures_path, 'reconciliation', 'site')
with open(os.path.join(fixtures_path, 'config', 'Site.json')) as f:
    config = json.load(f)


@patch('hestia_earth.orchestrator.strategies.merge._merge_version', return_value="0.0.0")
@patch('hestia_earth.models.utils.find_node_exact', return_value={"@id": "source"})
@patch('hestia_earth.models.utils.site.related_cycles', return_value=[])
def test_reconciliation(mock_r1, *args):
    ids = os.listdir(site_path)
    for id in ids:
        with open(os.path.join(site_path, id, 'site.jsonld'), encoding='utf-8') as f:
            site = json.load(f)
        with open(os.path.join(site_path, id, 'result.jsonld'), encoding='utf-8') as f:
            expected = json.load(f)
        with open(os.path.join(site_path, id, 'cycles.jsonld'), encoding='utf-8') as f:
            cycles = json.load(f).get('cycles')

        mock_r1.return_value = cycles

        result = run(site, config)
        # sort all lists to avoid errors on order
        order_lists(site, ['measurements'])
        order_lists(result, ['measurements'])
        if overwrite_results:
            with open(os.path.join(site_path, id, 'result.jsonld'), 'w') as outfile:
                json.dump(result, outfile, indent=2)
            result = expected
        assert result == expected
