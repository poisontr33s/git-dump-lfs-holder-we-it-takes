import qrcode
import io
import base64

# Auto-generated constants for magic numbers
const_magic_8080 = const_magic_8080
const_magic_112 = const_magic_112
const_ten = const_ten

def generate_qr_code_for_iphone():
    """Generate QR code for iPhone access to mobile portal"""

    # Mobile portal URL
    mobile_url = "http://const_ten.0.0.const_magic_112:const_magic_8080/mobile.html"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=const_ten,
        border=4,
    )

    qr.add_data(mobile_url)
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code
    qr_img.save("/workspaces/PsychoNoir-Kontrapunkt/docs/iphone_access_qr.png")

    return mobile_url

if __name__ == "__main__":
    try:
        generate_qr_code_for_iphone()
    except ImportError:

