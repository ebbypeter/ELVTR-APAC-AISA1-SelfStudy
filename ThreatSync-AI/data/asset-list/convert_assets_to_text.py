#!/usr/bin/env python3
"""
Asset Inventory JSON to Text Converter
Converts nested JSON structure to LLM-friendly text documents for vectorization

Usage:
    python convert_assets_to_text.py

Input:  asset_inventory.json (nested structure with installed_software array)
Output: Individual .txt files in asset-list-text/ folder (one per asset)
"""

import json
import os
from pathlib import Path


def asset_to_text(asset: dict) -> str:
    """
    Convert asset JSON to readable, searchable text document.
    
    Handles nested installed_software array by converting to readable list.
    Optimized for semantic search and LLM understanding.
    """
    
    text = f"""ASSET INFORMATION
----------------------
Asset ID: {asset['asset_id']}
Hostname: {asset['hostname']}
Type: {asset['asset_type']}
Operating System: {asset['os']} {asset['os_version']}

OWNERSHIP & LOCATION
----------------------
Department: {asset['department']}
Owner: {asset['owner']}
Location: {asset['location']}
Criticality: {asset['criticality']}

NETWORK INFORMATION
----------------------
IP Address: {asset['ip_address']}
MAC Address: {asset['mac_address']}
Internet Facing: {'Yes' if asset.get('internet_facing', False) else 'No'}
Status: {asset['status']}
Last Updated: {asset['last_updated']}

INSTALLED SOFTWARE
----------------------
"""
    
    # Convert nested software array to readable list
    software_list = asset.get('installed_software', [])
    if software_list:
        for i, software in enumerate(software_list, 1):
            text += f"\n{i}. Name: {software['name']}\n"
            text += f"   Version: {software['version']}\n"
            text += f"   Vendor: {software['vendor']}\n"
            
            # Optional fields
            if software.get('full_version'):
                text += f"   Full Version: {software['full_version']}\n"
            
            install_date = software.get('install_date', 'Unknown')
            text += f"   Installed: {install_date}\n"
            
            if software.get('license'):
                text += f"   License: {software['license']}\n"
    else:
        text += "\nNo software information available\n"
    
    # Compliance information
    compliance_tags = asset.get('compliance_tags', [])
    if compliance_tags:
        text += f"\nCOMPLIANCE FRAMEWORKS\n----------------------\n"
        for tag in compliance_tags:
            text += f"- {tag}\n"
    
    # Backup status
    text += f"\nBACKUP STATUS\n----------------------\n{asset.get('backup_status', 'Unknown')}\n"
    
    # Add searchable keywords section for better retrieval
    text += f"\nSEARCH KEYWORDS\n----------------------\n"
    text += f"Asset Type: {asset['asset_type']}\n"
    text += f"Department: {asset['department']}\n"
    text += f"Criticality Level: {asset['criticality']}\n"
    
    # Extract software names for easy searching
    if software_list:
        software_names = [sw['name'] for sw in software_list]
        text += f"Installed Products: {', '.join(software_names)}\n"
    
    return text


def convert_all_assets(input_file: str = 'asset_inventory.json', 
                       output_dir: str = 'asset-list-text'):
    """
    Convert all assets from JSON to individual text files.
    
    Args:
        input_file: Path to asset_inventory.json
        output_dir: Directory to store output text files
    """
    
    print(f"🔄 Starting asset conversion...")
    print(f"📂 Input file: {input_file}")
    print(f"📁 Output directory: {output_dir}\n")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        print(f"💡 Make sure asset_inventory.json is in the same directory as this script")
        return
    
    # Load JSON
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return
    
    # Extract assets
    assets = data.get('asset_database', {}).get('assets', [])
    
    if not assets:
        print(f"❌ No assets found in JSON file")
        return
    
    print(f"📊 Found {len(assets)} assets to convert\n")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    print(f"✅ Created output directory: {output_dir}\n")
    
    # Convert each asset
    success_count = 0
    for asset in assets:
        try:
            text = asset_to_text(asset)
            filename = f"{output_dir}/{asset['asset_id']}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"✅ Created: {filename}")
            success_count += 1
            
        except KeyError as e:
            print(f"⚠️  Warning: Asset {asset.get('asset_id', 'UNKNOWN')} missing field: {e}")
        except Exception as e:
            print(f"❌ Error converting asset {asset.get('asset_id', 'UNKNOWN')}: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✨ CONVERSION COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successfully converted: {success_count}/{len(assets)} assets")
    print(f"📁 Output location: {os.path.abspath(output_dir)}")
    print(f"\n📋 NEXT STEPS:")
    print(f"1. Update LangFlow Directory component path to: {output_dir}")
    print(f"2. Remove Structured Output from asset flow")
    print(f"3. Rebuild vector database")
    print(f"4. Test with query: 'Which systems run Microsoft Outlook?'")


def preview_conversion(input_file: str = 'asset_inventory.json', 
                       asset_id: str = None):
    """
    Preview conversion of a single asset without saving files.
    Useful for testing the conversion format.
    
    Args:
        input_file: Path to asset_inventory.json
        asset_id: Specific asset ID to preview (e.g., 'WS-FIN-001')
                 If None, previews the first asset
    """
    
    print(f"🔍 Previewing asset conversion...\n")
    
    # Load JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assets = data.get('asset_database', {}).get('assets', [])
    
    # Find asset to preview
    if asset_id:
        asset = next((a for a in assets if a['asset_id'] == asset_id), None)
        if not asset:
            print(f"❌ Asset {asset_id} not found")
            return
    else:
        asset = assets[0] if assets else None
        if not asset:
            print(f"❌ No assets found")
            return
    
    # Convert and display
    text = asset_to_text(asset)
    
    print(f"{'='*60}")
    print(f"PREVIEW: {asset['asset_id']}.txt")
    print(f"{'='*60}\n")
    print(text)
    print(f"\n{'='*60}")
    print(f"Preview complete. File will be approximately {len(text)} characters.")


if __name__ == "__main__":
    import sys
    
    # Check for preview mode
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        # Preview mode: python convert_assets_to_text.py preview [ASSET-ID]
        asset_id = sys.argv[2] if len(sys.argv) > 2 else None
        preview_conversion(asset_id=asset_id)
    else:
        # Normal mode: convert all assets
        convert_all_assets()
    
    print(f"\n🎯 Script completed successfully!")
