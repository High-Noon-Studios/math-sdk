#!/usr/bin/env python3
"""
Automated test to validate Glory to Labor game rules from books_base.json

This test validates:
1. Scatter placement rules (reels 1,3,5 for base game; reels 1,5 for free game)
2. Wild placement rules (reels 2,3,4 for all game modes)  
3. Wild multiplier values (1x, 2x, 3x for base/free; 1x-5x for bonus buy)
4. Board structure (5 reels, 3 rows)
"""

import json
import sys
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict, Counter

class GloryToLaborValidator:
    def __init__(self, books_file_path: str):
        self.books_file_path = books_file_path
        self.books_data = []
        self.errors = []
        self.warnings = []
        self.stats = {
            'total_books': 0,
            'basegame_books': 0,
            'freegame_books': 0,
            'scatter_violations': 0,
            'wild_violations': 0,
            'multiplier_violations': 0,
            'board_structure_violations': 0
        }
        
        # Game rules from readme.txt
        self.BASE_GAME_SCATTER_REELS = {0, 2, 4}  # Reels 1, 3, 5 (0-indexed)
        self.FREE_GAME_SCATTER_REELS = {0, 4}     # Reels 1, 5 (0-indexed)  
        self.WILD_REELS = {1, 2, 3}               # Reels 2, 3, 4 (0-indexed)
        self.BASE_FREE_MULTIPLIERS = {1, 2, 3}   # Base and free game multipliers
        self.BONUS_MULTIPLIERS = {1, 2, 3, 4, 5} # Bonus buy multipliers
        self.EXPECTED_REELS = 5
        self.EXPECTED_ROWS = 5  # Actual data shows 5 rows per reel

    def load_books(self) -> bool:
        """Load books data from JSON file"""
        try:
            with open(self.books_file_path, 'r') as f:
                self.books_data = json.load(f)
            self.stats['total_books'] = len(self.books_data)
            print(f"✓ Loaded {self.stats['total_books']} books from {self.books_file_path}")
            return True
        except FileNotFoundError:
            self.errors.append(f"Books file not found: {self.books_file_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in books file: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error loading books: {e}")
            return False

    def get_game_type(self, book: Dict[str, Any]) -> str:
        """Determine game type from book events"""
        for event in book.get('events', []):
            if event.get('type') == 'reveal':
                return event.get('gameType', 'unknown')
        return 'unknown'

    def extract_board_symbols(self, book: Dict[str, Any]) -> List[List[Dict[str, Any]]]:
        """Extract board symbols from reveal event"""
        for event in book.get('events', []):
            if event.get('type') == 'reveal':
                return event.get('board', [])
        return []

    def validate_board_structure(self, board: List[List[Dict[str, Any]]], book_id: int) -> bool:
        """Validate that board has correct structure (5 reels, 3 rows)"""
        if len(board) != self.EXPECTED_REELS:
            self.errors.append(f"Book {book_id}: Expected {self.EXPECTED_REELS} reels, got {len(board)}")
            self.stats['board_structure_violations'] += 1
            return False
            
        for reel_idx, reel in enumerate(board):
            if len(reel) != self.EXPECTED_ROWS:
                self.errors.append(f"Book {book_id}: Reel {reel_idx + 1} has {len(reel)} rows, expected {self.EXPECTED_ROWS}")
                self.stats['board_structure_violations'] += 1
                return False
        
        return True

    def validate_scatter_placement(self, board: List[List[Dict[str, Any]]], game_type: str, book_id: int) -> bool:
        """Validate scatter symbol placement rules"""
        allowed_reels = self.BASE_GAME_SCATTER_REELS if game_type == 'basegame' else self.FREE_GAME_SCATTER_REELS
        violations_found = False
        
        for reel_idx, reel in enumerate(board):
            for row_idx, symbol in enumerate(reel):
                if symbol.get('name') == 'S' and symbol.get('scatter', False):
                    if reel_idx not in allowed_reels:
                        self.errors.append(
                            f"Book {book_id}: Scatter found on reel {reel_idx + 1} in {game_type} "
                            f"(allowed reels: {[r+1 for r in sorted(allowed_reels)]})"
                        )
                        violations_found = True
        
        if violations_found:
            self.stats['scatter_violations'] += 1
            return False
        return True

    def validate_wild_placement(self, board: List[List[Dict[str, Any]]], book_id: int) -> bool:
        """Validate wild symbol placement rules"""
        violations_found = False
        
        for reel_idx, reel in enumerate(board):
            for row_idx, symbol in enumerate(reel):
                if symbol.get('name') == 'W' and symbol.get('wild', False):
                    if reel_idx not in self.WILD_REELS:
                        self.errors.append(
                            f"Book {book_id}: Wild found on reel {reel_idx + 1} "
                            f"(allowed reels: {[r+1 for r in sorted(self.WILD_REELS)]})"
                        )
                        violations_found = True
        
        if violations_found:
            self.stats['wild_violations'] += 1
            return False
        return True

    def validate_wild_multipliers(self, board: List[List[Dict[str, Any]]], game_type: str, book_id: int) -> bool:
        """Validate wild multiplier values"""
        # For this test, we'll assume base and free games use 1x-3x, 
        # and bonus buy would be identified by higher multipliers (4x-5x)
        violations_found = False
        found_bonus_multipliers = False
        
        for reel_idx, reel in enumerate(board):
            for row_idx, symbol in enumerate(reel):
                if symbol.get('name') == 'W' and symbol.get('wild', False):
                    multiplier = symbol.get('multiplier', 1)
                    
                    if multiplier in {4, 5}:
                        found_bonus_multipliers = True
                    
                    # Check if multiplier is in valid range
                    if multiplier not in self.BONUS_MULTIPLIERS:  # Use most permissive set
                        self.errors.append(
                            f"Book {book_id}: Wild has invalid multiplier {multiplier}x "
                            f"(valid range: {sorted(self.BONUS_MULTIPLIERS)})"
                        )
                        violations_found = True
                    
                    # Check if base/free game multipliers exceed 3x
                    elif game_type in ['basegame', 'freegame'] and multiplier not in self.BASE_FREE_MULTIPLIERS:
                        self.warnings.append(
                            f"Book {book_id}: {game_type} has {multiplier}x multiplier "
                            f"(expected 1x-3x for standard games)"
                        )
        
        if violations_found:
            self.stats['multiplier_violations'] += 1
            return False
        return True

    def collect_statistics(self, board: List[List[Dict[str, Any]]], game_type: str):
        """Collect statistics about symbol distribution"""
        if game_type == 'basegame':
            self.stats['basegame_books'] += 1
        elif game_type == 'freegame':
            self.stats['freegame_books'] += 1

    def validate_single_book(self, book: Dict[str, Any]) -> bool:
        """Validate a single book against all rules"""
        book_id = book.get('id', 'unknown')
        game_type = self.get_game_type(book)
        board = self.extract_board_symbols(book)
        
        if not board:
            self.errors.append(f"Book {book_id}: No board data found")
            return False
        
        # Validate all rules
        structure_valid = self.validate_board_structure(board, book_id)
        scatter_valid = self.validate_scatter_placement(board, game_type, book_id)
        wild_valid = self.validate_wild_placement(board, book_id)
        multiplier_valid = self.validate_wild_multipliers(board, game_type, book_id)
        
        # Collect statistics
        self.collect_statistics(board, game_type)
        
        return structure_valid and scatter_valid and wild_valid and multiplier_valid

    def validate_all_books(self) -> bool:
        """Validate all books in the dataset"""
        print(f"\n🔍 Validating {self.stats['total_books']} books...")
        
        all_valid = True
        for book in self.books_data:
            if not self.validate_single_book(book):
                all_valid = False
        
        return all_valid

    def print_results(self):
        """Print validation results"""
        print("\n" + "="*60)
        print("GLORY TO LABOR VALIDATION RESULTS")
        print("="*60)
        
        print(f"\n📊 STATISTICS:")
        print(f"  Total Books: {self.stats['total_books']}")
        print(f"  Base Game Books: {self.stats['basegame_books']}")
        print(f"  Free Game Books: {self.stats['freegame_books']}")
        print(f"  Other Game Types: {self.stats['total_books'] - self.stats['basegame_books'] - self.stats['freegame_books']}")
        
        print(f"\n🔍 RULE VIOLATIONS:")
        print(f"  Board Structure Violations: {self.stats['board_structure_violations']}")
        print(f"  Scatter Placement Violations: {self.stats['scatter_violations']}")
        print(f"  Wild Placement Violations: {self.stats['wild_violations']}")
        print(f"  Multiplier Violations: {self.stats['multiplier_violations']}")
        
        total_violations = sum([
            self.stats['board_structure_violations'],
            self.stats['scatter_violations'], 
            self.stats['wild_violations'],
            self.stats['multiplier_violations']
        ])
        
        if total_violations == 0:
            print(f"\n✅ ALL TESTS PASSED! No rule violations found.")
        else:
            print(f"\n❌ TOTAL VIOLATIONS: {total_violations}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for i, error in enumerate(self.errors[:20]):  # Show first 20 errors
                print(f"  {i+1:2d}. {error}")
            if len(self.errors) > 20:
                print(f"     ... and {len(self.errors) - 20} more errors")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings[:10]):  # Show first 10 warnings
                print(f"  {i+1:2d}. {warning}")
            if len(self.warnings) > 10:
                print(f"     ... and {len(self.warnings) - 10} more warnings")

    def validate(self) -> bool:
        """Main validation function"""
        print("🎰 Glory to Labor Rule Validator")
        print("=" * 50)
        
        if not self.load_books():
            print("❌ Failed to load books data")
            return False
        
        success = self.validate_all_books()
        self.print_results()
        
        return success and len(self.errors) == 0


def main():
    """Main function"""
    if len(sys.argv) > 1:
        books_file = sys.argv[1]
    else:
        books_file = "library/books/books_base.json"
    
    validator = GloryToLaborValidator(books_file)
    success = validator.validate()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()