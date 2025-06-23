import os

from asn1crypto import cms, x509


def extract_signature_info(p7s_path):
    try:
        with open(p7s_path, "rb") as f:
            content = f.read()
        content_info = cms.ContentInfo.load(content)
        signer_infos = content_info["content"]["signer_infos"]
        certs = content_info["content"]["certificates"]
        result = []
        for signer in signer_infos:
            sid = signer["sid"]
            serial = sid.chosen["serial_number"].native
            signer_cert = None
            for cert in certs:
                cert = x509.Certificate.load(cert.dump())
                if cert.serial_number == serial:
                    signer_cert = cert
                    break
            if signer_cert:
                subject = signer_cert.subject.native
                result.append(
                    {
                        "ПІБ": subject.get("common_name", "невідомо"),
                        "Організація": subject.get("organization_name", "невідомо"),
                        "Серійний номер": signer_cert.serial_number,
                    }
                )
        return result
    except Exception as e:
        return [{"Помилка": str(e)}]
