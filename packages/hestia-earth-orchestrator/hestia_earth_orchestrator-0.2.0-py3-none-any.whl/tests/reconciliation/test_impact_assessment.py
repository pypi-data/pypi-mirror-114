from unittest.mock import patch
import json
import os
from tests.utils import overwrite_results, fixtures_path, order_lists

from hestia_earth.orchestrator import run

impact_path = os.path.join(fixtures_path, 'reconciliation', 'impact-assessment')
cycle_path = os.path.join(fixtures_path, 'reconciliation', 'cycle')
site_path = os.path.join(fixtures_path, 'reconciliation', 'site')
with open(os.path.join(fixtures_path, 'config', 'ImpactAssessment.json')) as f:
    config = json.load(f)


@patch('hestia_earth.orchestrator.strategies.merge._merge_version', return_value="0.0.0")
def test_reconciliation(*args):
    ids = os.listdir(impact_path)
    for id in ids:
        with open(os.path.join(impact_path, id, 'impact-assessment.jsonld'), encoding='utf-8') as f:
            impact = json.load(f)
        with open(os.path.join(impact_path, id, 'result.jsonld'), encoding='utf-8') as f:
            expected = json.load(f)

        # load the corresponding Cycle
        with open(os.path.join(cycle_path, impact['cycle']['@id'], 'result.jsonld'), encoding='utf-8') as f:
            cycle = json.load(f)
        # load the corresponding Site
        with open(os.path.join(site_path, cycle['site']['@id'], 'result.jsonld'), encoding='utf-8') as f:
            cycle['site'] = json.load(f)

        original_cycle = impact['cycle']
        impact['cycle'] = cycle
        # remove cycle @id to prevent running since already included
        impact['cycle']['@id'] = None
        result = run(impact, config)
        # restore cycle to avoid having diffs
        impact['cycle'] = original_cycle
        result['cycle'] = original_cycle
        # sort all lists to avoid errors on order
        order_lists(impact, ['emissionsResourceUse', 'impacts'])
        order_lists(result, ['emissionsResourceUse', 'impacts'])
        if overwrite_results:
            with open(os.path.join(impact_path, id, 'result.jsonld'), 'w') as outfile:
                json.dump(result, outfile, indent=2)
            result = expected
        assert result == expected
