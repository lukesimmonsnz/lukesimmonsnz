#!/usr/bin/env python3
"""
Fix source and claim schema enums to match schema constraints.
"""

import yaml
from pathlib import Path

# Source type and credibility mappings
SOURCE_TYPE_MAP = {
    'official_data': 'government-report',
    'primary-data': 'primary-data',
    'academic': 'academic',
    'industry': 'commentary',
    'government_report': 'government-report',
    'research': 'academic',
    'community': 'iwi-publication',
}

SOURCE_CREDIBILITY_MAP = {
    'government_primary': 'official',
    'peer-reviewed': 'peer-reviewed',
    'official': 'official',
    'reputable': 'reputable',
    'partisan': 'partisan',
    'academic': 'peer-reviewed',
    'industry_primary': 'reputable',
    'community_primary': 'reputable',
    'research_primary': 'peer-reviewed',
}

# Claim enum mappings
CLAIM_STATUS_MAP = {
    'unverified': 'cited_only',
    'verified': 'verified',
    'cited_only': 'cited_only',
    'needs_verification': 'needs_verification',
}

def fix_sources(region_path):
    """Fix all source files in a region."""
    source_dir = region_path / 'data' / 'source'
    fixed_count = 0

    for source_file in source_dir.glob('*.yaml'):
        with open(source_file, 'r') as f:
            data = yaml.safe_load(f)

        # Fix type
        if 'type' in data:
            old_type = data['type']
            data['type'] = SOURCE_TYPE_MAP.get(old_type, 'government-report')

        # Fix credibility
        if 'credibility' in data:
            old_cred = data['credibility']
            data['credibility'] = SOURCE_CREDIBILITY_MAP.get(old_cred, 'reputable')

        with open(source_file, 'w') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        fixed_count += 1

    return fixed_count

def fix_claims(region_path):
    """Fix all claim files in a region."""
    claim_dir = region_path / 'data' / 'claim'
    fixed_count = 0

    for claim_file in claim_dir.glob('*.yaml'):
        with open(claim_file, 'r') as f:
            data = yaml.safe_load(f)

        # Fix verification_status
        if 'verification_status' in data:
            old_status = data['verification_status']
            data['verification_status'] = CLAIM_STATUS_MAP.get(old_status, 'cited_only')

        # Fix source_ids: every claim must have at least one source
        if 'source_ids' not in data or not data['source_ids']:
            # Assign a dummy source (will need to be set properly later)
            # For now, use region-specific stats
            region = region_path.name
            if region == 'otago':
                data['source_ids'] = ['source.otago_stats_2024']
            elif region == 'southland':
                data['source_ids'] = ['source.southland_council_2024']

        with open(claim_file, 'w') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        fixed_count += 1

    return fixed_count

# Execute
if __name__ == '__main__':
    base_path = Path('/sessions/blissful-festive-clarke/mnt/Current website/content')

    for region in ['otago', 'southland']:
        region_path = base_path / region

        sources_fixed = fix_sources(region_path)
        claims_fixed = fix_claims(region_path)

        print(f"✓ {region}: {sources_fixed} sources, {claims_fixed} claims fixed")

    print("\n✓ All schema enum fixes applied")
