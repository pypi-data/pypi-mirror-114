from unittest.mock import patch
import json
import os
from tests.utils import overwrite_results, fixtures_path, order_lists

from hestia_earth.orchestrator import run

cycle_path = os.path.join(fixtures_path, 'reconciliation', 'cycle')
site_path = os.path.join(fixtures_path, 'reconciliation', 'site')
with open(os.path.join(fixtures_path, 'config', 'Cycle.json')) as f:
    config = json.load(f)


# skip aggregated model as the data evolves over time, but keep in Config for reference
@patch('hestia_earth.models.cycle.input.aggregated.run', return_value=[])
@patch('hestia_earth.orchestrator.strategies.merge._merge_version', return_value="0.0.0")
def test_reconciliation(*args):
    ids = os.listdir(cycle_path)
    for id in ids:
        with open(os.path.join(cycle_path, id, 'cycle.jsonld'), encoding='utf-8') as f:
            cycle = json.load(f)
        with open(os.path.join(cycle_path, id, 'result.jsonld'), encoding='utf-8') as f:
            expected = json.load(f)

        # load the corresponding site
        with open(os.path.join(site_path, cycle['site']['@id'], 'result.jsonld'), encoding='utf-8') as f:
            site = json.load(f)

        original_site = cycle['site']
        cycle['site'] = site
        # remove site @id to prevent running since already included
        cycle['site']['@id'] = None
        result = run(cycle, config)
        # restore site to avoid having diffs
        cycle['site'] = original_site
        result['site'] = original_site
        # sort all lists to avoid errors on order
        order_lists(cycle, ['inputs', 'products', 'emissions'])
        order_lists(result, ['inputs', 'products', 'emissions'])
        if overwrite_results:
            with open(os.path.join(cycle_path, id, 'result.jsonld'), 'w') as outfile:
                json.dump(result, outfile, indent=2)
            result = expected
        assert result == expected
