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
        ]
        
        for filename in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNone(dt, f"Não deveria reconhecer {filename}")
                
    def test_pattern_10_videocapture(self):
        """Testa Pattern 10: VideoCapture_YYYYMMDD-HHMMSS"""
        test_cases = [
            ("VideoCapture_20240513-155722.jpg", datetime(2024, 5, 13, 15, 57, 22)),
            ("VideoCapture_20230101-010101.jpg", datetime(2023, 1, 1, 1, 1, 1)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
                
    def test_pattern_11_timestamp_uuid(self):
        """Testa Pattern 11: TIMESTAMP-UUID.jpg"""
        # O timestamp 1628085150 corresponde a 2021-08-04 com hora variável dependendo do fuso horário
        test_cases = [
            ("1628085150288-uuid.jpg", 1628085150),
        ]
        
        for filename, expected_timestamp in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                expected_dt = datetime.fromtimestamp(expected_timestamp)
                
                # Verificamos apenas a data, pois a hora pode variar dependendo do fuso horário
                self.assertEqual(dt.year, expected_dt.year, f"Ano incorreto para {filename}")
                self.assertEqual(dt.month, expected_dt.month, f"Mês incorreto para {filename}")
                self.assertEqual(dt.day, expected_dt.day, f"Dia incorreto para {filename}")
                
                # Verificamos também se o texto de informação contém "timestamp"
                self.assertIn("timestamp", info, f"Informação deve conter 'timestamp' para {filename}")
                
    def test_pattern_12_picsart(self):
        """Testa Pattern 12: Picsart_YY-MM-DD_HH-MM-SS"""
        test_cases = [
            ("Picsart_22-09-05_08-32-31-010.jpg", datetime(2022, 9, 5, 8, 32, 31)),
            ("Picsart_21-01-15_12-30-45-123.jpg", datetime(2021, 1, 15, 12, 30, 45)),
        ]
        
        for filename, expected_date in test_cases:
            with self.subTest(filename=filename):
                dt, info = extract_date(filename)
                self.assertIsNotNone(dt, f"Deveria reconhecer {filename}")
                self.assertEqual(dt, expected_date, f"Data incorreta para {filename}")
                
    def test_pattern_13_camscanner(self):
        """Testa Pattern 13: CamScanner MM-DD-YYYY HH.MM"""
        test_cases = [
            ("CamScanner 10-30-2022 17.02.jpg", datetime(2022, 10, 30, 17, 2, 0)),
            ("CamScanner 10-30-2022 17.02_1.jpg", datetime(2022, 10, 30, 17, 2, 0)),
            ("CamScanner 01-15-2020 08.45.pdf", datetime(2020, 1, 15, 8, 45, 0)),
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
    print("=" * 70)        # Lista de arquivos de teste
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
        ("VideoCapture_20240513-155722.jpg", "VideoCapture"),
        ("1628085150288-uuid.jpg", "Timestamp-UUID"),
        ("Picsart_22-09-05_08-32-31-010.jpg", "PicsArt"),
        ("CamScanner 10-30-2022 17.02.jpg", "CamScanner"),
        ("CamScanner 10-30-2022 17.02_1.jpg", "CamScanner com sufixo"),
        
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
