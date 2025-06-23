import io
import logging
import sys

import asn1crypto.cms
import asn1crypto.pem

# Забезпечити правильне виведення у консоль з UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

logging.basicConfig(level=logging.INFO)


def extract_signature_info(file_path):
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read()

        if asn1crypto.pem.detect(raw_data):
            _, _, raw_data = asn1crypto.pem.unarmor(raw_data)

        content_info = asn1crypto.cms.ContentInfo.load(raw_data)
        signer_infos = content_info["content"]["signer_infos"]

        result = []
        for signer in signer_infos:
            sid = signer["sid"]
            signer_info = {
                "issuer": sid.chosen["issuer"].human_friendly,
                "serial_number": sid.chosen["serial_number"].native,
            }
            result.append(signer_info)

        return result
    except Exception as e:
        logging.error(f"Помилка при витягуванні підпису: {e}")
        return [{"error": str(e)}]
