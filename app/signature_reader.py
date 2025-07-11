from asn1crypto import cms
from typing import List, Dict


def extract_signature_info(p7s_path: str) -> List[Dict[str, str]]:
    """
    Зчитує файл P7S та повертає список словників з інформацією
    про підписників: issuer і serial_number.
    """
    try:
        with open(p7s_path, "rb") as f:
            content = f.read()
        content_info = cms.ContentInfo.load(content)
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
        return []
