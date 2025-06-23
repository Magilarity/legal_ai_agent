import logging

import asn1crypto.cms
import asn1crypto.pem

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def extract_signature_info(file_path: str) -> list:
    """
    Повертає список словників із полями issuer/serial_number.
    Якщо файл не валідний PKCS#7, повертає пустий список.
    """
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read()

        # Якщо PEM-обгортка, знімаємо її
        if asn1crypto.pem.detect(raw_data):
            _, _, raw_data = asn1crypto.pem.unarmor(raw_data)

        content_info = asn1crypto.cms.ContentInfo.load(raw_data)
        signer_infos = content_info["content"]["signer_infos"]
        certs = content_info["content"].get("certificates", [])

        result = []
        for signer in signer_infos:
            sid = signer["sid"]
            serial = sid.chosen["serial_number"].native
            # Знаходимо сертифікат за серійником
            signer_cert = None
            for cert in certs:
                cert_obj = (
                    cert
                    if isinstance(cert, asn1crypto.x509.Certificate)
                    else asn1crypto.x509.Certificate.load(cert.dump())
                )
                if cert_obj.serial_number == serial:
                    signer_cert = cert_obj
                    break
            issuer = signer_cert.subject.human_friendly if signer_cert else "Н/Д"
            result.append({"issuer": issuer, "serial_number": serial})

        return result

    except (ValueError, TypeError) as e:
        # Не валідний PKCS#7 або не вдалося розпізнати — просто повертаємо пустий список
        logging.warning(f"Не валідний .p7s або помилка парсингу: {e}")
        return []
    except Exception as e:
        logging.error(f"Помилка при витягуванні підпису: {e}")
        return [{"error": str(e)}]
