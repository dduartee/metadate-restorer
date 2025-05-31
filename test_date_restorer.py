#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes para o Date Restorer

Este arquivo contém testes abrangentes para verificar se o script está
funcionando corretamente com diferentes padrões de nomes de arquivo.
"""

import os
import sys
import tempfile
import shutil
import unittest
from datetime import datetime
from date_restorer import extract_date

class TestDateRestorer(unittest.TestCase):
    
    def setUp(self):
        """Configura o ambiente de teste"""
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
    
    def test_pattern_1_digital_camera(self):
        """Testa Pattern 1: Câmeras digitais com formato YYYYMMDD_HHMMSS"""
        test_cases = [
            ("20181128_110755.jpg", datetime(2018, 11, 28, 11, 7, 55)),
            ("IMG_20180507_192217158.jpg", datetime(2018, 5, 7, 19, 22, 17)),
            ("20200101_000000.png", datetime(2020, 1, 1, 0, 0, 0)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
    
    def test_pattern_2_whatsapp(self):
        """Testa Pattern 2: WhatsApp com formato YYYY-MM-DD"""
        test_cases = [
            ("WhatsApp Image 2018-11-27 at 18.41.02.png", datetime(2018, 11, 27, 18, 41, 2)),
            ("WhatsApp Video 2020-05-15.mp4", datetime(2020, 5, 15, 0, 0, 0)),
            ("Document 2019-12-31.pdf", datetime(2019, 12, 31, 0, 0, 0)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
    
    def test_pattern_3_timestamps_validos(self):
        """Testa Pattern 3: Timestamps válidos"""
        test_cases = [
            # Timestamps com prefixos conhecidos
            ("FB_IMG_1545742864733.jpg", 1545742864),  # 2018-12-25
            ("IMG_1531699202.jpg", 1531699202),        # 2018-07-16
            
            # Timestamps standalone
            ("1577836800.jpg", 1577836800),            # 2020-01-01
            ("946684800.jpg", 946684800),              # 2000-01-01 (Y2K)
            # Note: 0.jpg removed because 0 has only 1 digit, below minimum of 9
        ]
        
        for filename, expected_timestamp in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                expected_dt = datetime.fromtimestamp(expected_timestamp)
                self.assertEqual(dt, expected_dt, f"Data incorreta para {filename}")
    
    def test_pattern_3_timestamps_invalidos(self):
        """Testa Pattern 3: Timestamps que devem ser rejeitados"""
        test_cases = [
            # Números grandes que não são timestamps
            "130904361_220496336181674_1278815373953210947_n.jpg",
            "12345678901234567890_invalid.jpg",
            "999999999999999999999_super_long.jpg",
            "random_123456789012345_numbers.jpg",
            
            # Timestamps no futuro (qualquer data após a data atual)
            "2556144000.jpg",  # 2051
            "4102444800.jpg",  # 2100
            "9999999999.jpg",  # Data futura
            
            # Patterns que não devem ser reconhecidos como timestamps
            "arquivo_1234567890_outro.jpg",  # Número no meio do nome
            "foto1234567890qualquercoisa.jpg",  # Sem separadores
        ]
        
        for filename in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNone(dt, f"NÃO deveria reconhecer {filename}")
    
    def test_pattern_4_screenshots(self):
        """Testa Pattern 4: Screenshots"""
        test_cases = [
            ("Screenshot_20200101-151016_Calendar.jpg", datetime(2020, 1, 1, 15, 10, 16)),
            ("Screenshot_20200224-162219.jpg", datetime(2020, 2, 24, 16, 22, 19)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
    
    def test_pattern_5_whatsapp_video(self):
        """Testa Pattern 5: Vídeos do WhatsApp"""
        test_cases = [
            ("VID-20200615-WA0127.mp4", datetime(2020, 6, 15, 0, 0, 0)),
            ("VID-20181225-WA0001.mp4", datetime(2018, 12, 25, 0, 0, 0)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
    
    def test_pattern_6_whatsapp_image(self):
        """Testa Pattern 6: Imagens do WhatsApp"""
        test_cases = [
            ("IMG-20181225-WA0014.jpg", datetime(2018, 12, 25, 0, 0, 0)),
            ("IMG-20181218-WA0002.jpeg", datetime(2018, 12, 18, 0, 0, 0)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
    
    def test_pattern_7_android_photos(self):
        """Testa Pattern 7: Fotos do Android"""
        test_cases = [
            ("Photo_20200101_123059.jpg", datetime(2020, 1, 1, 12, 30, 59)),
            ("Photo_20190630_235959.jpg", datetime(2019, 6, 30, 23, 59, 59)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
    
    def test_pattern_8_date_time_separated(self):
        """Testa Pattern 8: Data e hora separadas"""
        test_cases = [
            ("2020-01-01 12.30.59.jpg", datetime(2020, 1, 1, 12, 30, 59)),
            ("2019-12-31 23.59.59.png", datetime(2019, 12, 31, 23, 59, 59)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
    
    def test_pattern_9_jpeg_smartphone(self):
        """Testa Pattern 9: JPEG de smartphones"""
        test_cases = [
            ("JPEG_20200722_183656.jpg", datetime(2020, 7, 22, 18, 36, 56)),
            ("JPEG_20190101_000000.jpg", datetime(2019, 1, 1, 0, 0, 0)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
    
    def test_arquivos_nao_reconhecidos(self):
        """Testa arquivos que não devem ser reconhecidos"""
        test_cases = [
            "arquivo_qualquer.jpg",
            "foto_sem_data.png",
            "video.mp4",
            "documento.pdf",
            "nome_estranho_123.jpg",
        ]
        
        for filename in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNone(dt, f"NÃO deveria reconhecer {filename}")
    
    def test_normalize_digits(self):
        """Testa a normalização de dígitos unicode"""
        from date_restorer import normalize_digits
        
        test_cases = [
            ("٢٠٢٠١٢٢٥_١٢٣٠٥٩.jpg", "20201225_123059.jpg"),
            ("۲۰۲۰۱۲۲۵_۱۲۳۰۵۹.jpg", "20201225_123059.jpg"),
            ("20201225_123059.jpg", "20201225_123059.jpg"),  # Já normalizado
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input=input_str):
                result = normalize_digits(input_str)
                self.assertEqual(result, expected)


def run_manual_tests():
    """
    Executa testes manuais mostrando os resultados na tela
    """
    print("=" * 70)
    print("TESTES MANUAIS DO DATE RESTORER")
    print("=" * 70)
    
    # Lista de arquivos de teste
    test_files = [
        # Padrões válidos
        ("20181128_110755.jpg", "Câmera digital"),
        ("IMG_20180507_192217158.jpg", "Câmera com prefixo IMG"),
        ("WhatsApp Image 2018-11-27 at 18.41.02.png", "WhatsApp com hora"),
        ("WhatsApp Video 2020-05-15.mp4", "WhatsApp sem hora"),
        ("FB_IMG_1545742864733.jpg", "Facebook timestamp"),
        ("1577836800.jpg", "Timestamp standalone"),
        ("946684800.jpg", "Timestamp Y2K (2000)"),
        ("Screenshot_20200101-151016_Calendar.jpg", "Screenshot com app"),
        ("Screenshot_20200224-162219.jpg", "Screenshot simples"),
        ("VID-20200615-WA0127.mp4", "Vídeo WhatsApp"),
        ("IMG-20181225-WA0014.jpg", "Imagem WhatsApp"),
        ("Photo_20200101_123059.jpg", "Foto Android"),
        ("2020-01-01 12.30.59.jpg", "Data e hora separadas"),
        ("JPEG_20200722_183656.jpg", "JPEG smartphone"),
        
        # Padrões inválidos
        ("130904361_220496336181674_1278815373953210947_n.jpg", "Rede social (inválido)"),
        ("12345678901234567890_invalid.jpg", "Números grandes (inválido)"),
        ("999999999999999999999_super_long.jpg", "Números muito grandes (inválido)"),
        ("2556144000.jpg", "Timestamp futuro (inválido)"),
        ("random_123456789012345_numbers.jpg", "Números aleatórios (inválido)"),
        ("arquivo_qualquer.jpg", "Sem padrão (inválido)"),
    ]
    
    successful = 0
    failed = 0
    
    for filename, description in test_files:
        dt, info = extract_date(filename)
        status = "✅ RECONHECIDO" if dt else "❌ NÃO RECONHECIDO"
        
        if dt:
            print(f"{status:15} | {filename:50} | {dt} | {description}")
            successful += 1
        else:
            print(f"{status:15} | {filename:50} | {'---':19} | {description}")
            failed += 1
    
    print("=" * 70)
    print(f"RESUMO: {successful} reconhecidos, {failed} não reconhecidos")
    print("=" * 70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Testes para o Date Restorer")
    parser.add_argument("--manual", action="store_true", help="Executa testes manuais")
    parser.add_argument("--unittest", action="store_true", help="Executa testes unitários")
    
    args = parser.parse_args()
    
    if args.manual:
        run_manual_tests()
    elif args.unittest:
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        # Se nenhuma opção específica for escolhida, executa ambos
        print("Executando testes manuais...")
        run_manual_tests()
        print("\n\nExecutando testes unitários...")
        unittest.main(argv=[''], exit=False, verbosity=2)
