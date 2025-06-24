import logging

import asn1crypto.cms
import asn1crypto.pem
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def extract_signature_info(file_path: str) -> List[Dict[str, str]]:
    """
    Повертає список словників із полями issuer/serial_number.
    Якщо файл не є валідним PKCS#7, повертається порожній список.
    """
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        content_info = asn1crypto.cms.ContentInfo.load(content)
        signer_infos = content_info["content"]["signer_infos"]
        certs = content_info["content"]["certificates"]
        result: List[Dict[str, str]] = []
        for signer in signer_infos:
            sid = signer["sid"]
            serial = sid.chosen["serial_number"].native
            signer_cert = None
            for cert in certs:
                if cert.chosen.serial_number == serial:
                    signer_cert = cert
                    break
            issuer = signer_cert.chosen.issuer.human_friendly if signer_cert else ""
            result.append({"issuer": issuer, "serial_number": str(serial)})
        return result
    except Exception:
        logging.error("Failed to parse signature file")
        return []
