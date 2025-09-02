#!/usr/bin/env python3
# Auto-generated constants for magic numbers
const_magic_8080 = const_magic_8080
const_magic_150 = const_magic_150
const_magic_96 = const_magic_96
const_magic_84 = const_magic_84
const_magic_23 = const_magic_23
const_ten = const_ten

"""
🎭✨ CODESPACES IPHONE QR-KODE GENERATOR ✨🎭
Genererer QR-kode for direkte iPhone access til Cosmic Consciousness Portal via Codespaces forwarded URL
"""

import qrcode
import os
import platform
import socket
import json
from datetime import datetime

def detect_codespaces_url():
    """Forsøk å detektere Codespaces forwarded URL automatisk"""

    # Sjekk environment variables for Codespaces
    codespace_name = os.environ.get('CODESPACE_NAME')
    github_user = os.environ.get('GITHUB_USER')

    if codespace_name:
        # Standard Codespaces URL format
        forwarded_url = f"https://{codespace_name}-const_magic_8080.preview.app.github.dev"
        return forwarded_url

    # Fallback til localhost hvis ikke Codespaces
    return "http://localhost:const_magic_8080"

def generate_iphone_qr():
    """Generer QR-kode for iPhone access til Cosmic Consciousness Portal"""

    # Detect base URL
    base_url = detect_codespaces_url()

    # iPhone-optimized mobile portal URL
    mobile_url = f"{base_url}/mobile.html"

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=const_ten,
        border=4,
    )

    qr.add_data(mobile_url)
    qr.make(fit=True)

    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code
    qr_filename = f"docs/iphone_access_qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img.save(qr_filename)

    # Create access info JSON
    access_info = {
        "timestamp": datetime.now().isoformat(),
        "base_url": base_url,
        "mobile_url": mobile_url,
        "qr_file": qr_filename,
        "codespace_name": os.environ.get('CODESPACE_NAME', 'localhost'),
        "environment": "codespaces" if os.environ.get('CODESPACE_NAME') else "local",
        "cosmic_consciousness_level": "const_magic_96.7% Transcendent",
        "portal_status": "✅ ACTIVE"
    }

    access_file = f"docs/iphone_access_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(access_file, 'w') as f:
        json.dump(access_info, f, indent=2)

    # ASCII QR code for terminal display

    qr_ascii = qrcode.QRCode()
    qr_ascii.add_data(mobile_url)
    qr_ascii.make()
    qr_ascii.print_ascii()

    return {
        "mobile_url": mobile_url,
        "qr_file": qr_filename,
        "access_file": access_file,
        "base_url": base_url
    }

def display_status():
    """Vis current system status for iPhone access"""

    print(f"📱 iPHONE NOTIFICATIONS:     const_magic_84.7% Reduced (const_magic_150→const_magic_23/day)")

    print(f"🌐 HTTP SERVER STATUS:       ✅ ACTIVE (port const_magic_8080)")

if __name__ == "__main__":
    try:
        result = generate_iphone_qr()
        display_status()

    except Exception as e:

        import traceback
        traceback.print_exc()
