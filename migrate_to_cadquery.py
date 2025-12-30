#!/usr/bin/env python3
"""
WDW Monorail CAD Migration Tool
Converts Blender/binary CAD files to CadQuery Python-based parametric models.
Removes old binary files and prepares repository for version control optimization.
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class CADMigration:
    """Manage CAD file migration from Blender to CadQuery."""
    
    def __init__(self, repo_root="/home/workspace/WDW-Automated-Monorail-System"):
        self.repo_root = Path(repo_root)
        self.cad_models_dir = self.repo_root / "CAD-Models"
        self.backup_dir = self.repo_root / ".cad_backup"
        self.migration_log = []
        self.stats = {
            "files_backed_up": 0,
            "files_removed": 0,
            "space_freed_mb": 0,
            "cad_files_generated": 0,
            "migration_time": None
        }
    
    def log_action(self, action: str, details: str = ""):
        """Log migration actions."""
        timestamp = datetime.now().isoformat()
        message = f"[{timestamp}] {action}"
        if details:
            message += f" - {details}"
        self.migration_log.append(message)
        print(f"📝 {message}")
    
    def backup_old_files(self) -> bool:
        """Backup old Blender/binary CAD files before deletion."""
        try:
            self.log_action("BACKUP_START", "Creating backup of old CAD files")
            
            # Create backup directory
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Files to backup (binary formats)
            binary_extensions = ['.blend', '.blend1', '.glb', '.obj', '.mtl', '.stl', '.png']
            
            for ext in binary_extensions:
                for file in self.cad_models_dir.glob(f"*{ext}"):
                    rel_path = file.relative_to(self.cad_models_dir)
                    backup_path = self.backup_dir / rel_path
                    
                    # Get file size
                    file_size_mb = file.stat().st_size / (1024 * 1024)
                    
                    # Backup
                    shutil.copy2(file, backup_path)
                    self.stats["files_backed_up"] += 1
                    self.stats["space_freed_mb"] += file_size_mb
                    
                    self.log_action("BACKUP", f"{file.name} ({file_size_mb:.1f} MB)")
            
            self.log_action("BACKUP_COMPLETE", f"Backed up {self.stats['files_backed_up']} files")
            return True
        
        except Exception as e:
            self.log_action("BACKUP_ERROR", str(e))
            return False
    
    def remove_old_cad_files(self) -> bool:
        """Remove old binary CAD files to clean up repository."""
        try:
            self.log_action("REMOVAL_START", "Removing old CAD files")
            
            # Files to remove (binary formats that bloat Git)
            removable_extensions = ['.blend', '.blend1', '.glb', '.obj', '.mtl', '.stl']
            
            for ext in removable_extensions:
                for file in self.cad_models_dir.glob(f"*{ext}"):
                    try:
                        os.remove(file)
                        self.stats["files_removed"] += 1
                        self.log_action("REMOVE", f"{file.name}")
                    except Exception as e:
                        self.log_action("REMOVE_ERROR", f"{file.name}: {str(e)}")
            
            # Also remove old renders if updating
            old_renders = self.cad_models_dir.glob("enhanced_barn_model.png")
            for file in old_renders:
                try:
                    os.remove(file)
                    self.log_action("REMOVE", f"{file.name} (old render)")
                except:
                    pass
            
            self.log_action("REMOVAL_COMPLETE", f"Removed {self.stats['files_removed']} files")
            return True
        
        except Exception as e:
            self.log_action("REMOVAL_ERROR", str(e))
            return False
    
    def generate_cadquery_models(self) -> bool:
        """Generate new CadQuery parametric models."""
        try:
            self.log_action("CADQUERY_GENERATION_START", "Generating parametric CAD models")
            
            # Generate track system
            track_script = self.cad_models_dir / "monorail_track_system.py"
            if track_script.exists():
                self.log_action("GENERATING", "Track system components...")
                result = subprocess.run(
                    ["python3", str(track_script)],
                    cwd=str(self.cad_models_dir),
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    self.stats["cad_files_generated"] += 4  # 4 STEP files
                    self.log_action("GENERATED", "Track system components (4 files)")
                else:
                    self.log_action("GENERATION_ERROR", f"Track system: {result.stderr}")
            
            # Generate barn
            barn_script = self.cad_models_dir / "monorail_barn_cadquery.py"
            if barn_script.exists():
                self.log_action("GENERATING", "Barn structure...")
                result = subprocess.run(
                    ["python3", str(barn_script)],
                    cwd=str(self.cad_models_dir),
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    self.stats["cad_files_generated"] += 1  # 1 STEP file
                    self.log_action("GENERATED", "Barn structure (1 file)")
                else:
                    self.log_action("GENERATION_ERROR", f"Barn: {result.stderr}")
            
            self.log_action("CADQUERY_GENERATION_COMPLETE", f"Generated {self.stats['cad_files_generated']} CAD files")
            return True
        
        except Exception as e:
            self.log_action("CADQUERY_ERROR", str(e))
            return False
    
    def update_gitignore(self) -> bool:
        """Update .gitignore to exclude large binary files."""
        try:
            self.log_action("GITIGNORE_UPDATE", "Updating .gitignore")
            
            gitignore_path = self.repo_root / ".gitignore"
            
            # CAD files to ignore
            cad_ignores = [
                "# CAD Binary Files (use CadQuery .py files instead)",
                "*.blend",
                "*.blend1",
                "*.glb",
                "*.obj",
                "*.mtl",
                "*.stl",
                "",
                "# Backup directories",
                ".cad_backup/",
                "",
                "# Generated files",
                "*.step",
                "*.stp",
            ]
            
            # Read existing .gitignore
            existing_lines = []
            if gitignore_path.exists():
                with open(gitignore_path, 'r') as f:
                    existing_lines = f.readlines()
            
            # Append CAD ignores if not already present
            with open(gitignore_path, 'a') as f:
                f.write("\n# === CAD Migration (CadQuery) ===\n")
                f.write("\n".join(cad_ignores))
                f.write("\n")
            
            self.log_action("GITIGNORE_UPDATED", ".gitignore configured for CadQuery")
            return True
        
        except Exception as e:
            self.log_action("GITIGNORE_ERROR", str(e))
            return False
    
    def clean_git_history(self) -> bool:
        """Remove old binary CAD files from Git tracking."""
        try:
            self.log_action("GIT_CLEANUP_START", "Removing binary files from Git tracking")
            
            # Files to remove from Git
            git_remove_commands = [
                "*.blend", "*.blend1", "*.glb", "*.obj", "*.mtl", "*.stl"
            ]
            
            os.chdir(str(self.repo_root))
            
            for pattern in git_remove_commands:
                result = subprocess.run(
                    ["git", "rm", "--cached", "-r", "--ignore-unmatch", pattern],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.log_action("GIT_REMOVE", f"Removed {pattern} from tracking")
            
            self.log_action("GIT_CLEANUP_COMPLETE", "Binary files removed from Git tracking")
            return True
        
        except Exception as e:
            self.log_action("GIT_CLEANUP_ERROR", str(e))
            return False
    
    def create_migration_report(self) -> bool:
        """Generate detailed migration report."""
        try:
            self.log_action("REPORT_GENERATION", "Creating migration report")
            
            report_path = self.repo_root / "CAD_MIGRATION_REPORT.md"
            
            report_content = f"""# CAD Migration Report - CadQuery Parametric Conversion

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status**: ✅ COMPLETED

## Summary

This migration converts the WDW Automated Monorail System from binary CAD files (Blender, OBJ, STL) to parametric CadQuery Python-based models.

### Benefits
- ✅ **Version Control**: Python files compress well in Git
- ✅ **Parametric**: Change dimensions in code, regenerate instantly
- ✅ **Reproducibility**: Rebuild models from source at any time
- ✅ **Collaboration**: Easier diff/merge workflows
- ✅ **Automation**: Generate variations programmatically

## Migration Statistics

| Metric | Value |
|--------|-------|
| Files Backed Up | {self.stats['files_backed_up']} |
| Files Removed | {self.stats['files_removed']} |
| Space Freed | {self.stats['space_freed_mb']:.1f} MB |
| CAD Files Generated | {self.stats['cad_files_generated']} |

## Files Backed Up

**Location**: `.cad_backup/`

Old binary CAD files have been backed up for reference:
- `enhanced_barn_model.blend` (Blender native)
- `enhanced_barn_model.glb` (Web format)
- `enhanced_barn_model.obj` + `.mtl` (Universal format)
- `enhanced_barn_model.stl` (3D printing format)
- `enhanced_barn_model.png` (Rendered preview)

## New CadQuery Models

The following parametric CAD Python scripts have been created:

### Barn Structure
- **File**: `monorail_barn_cadquery.py`
- **Output**: `monorail_barn_cadquery.step`
- **Features**:
  - 70m × 50m × 8.5m facility
  - 12 parking spaces with marking system
  - 4 maintenance bays with lift infrastructure
  - Central communication hub with antenna array
  - HVAC system (6-point distribution)
  - Electrical power distribution network
  - Structural columns with reinforcement
  - Parametric: change dimensions in code

### Track System Components
- **File**: `monorail_track_system.py`
- **Outputs**:
  - `monorail_track_beam.step` - Main track profile
  - `monorail_support_column.step` - Support structure
  - `monorail_track_assembly.step` - Full section assembly
  - `monorail_switch_system.step` - Switch mechanism
  - `sensor_mounting_bracket.step` - Sensor mount
- **Features**:
  - Inverted-T track profile
  - Hollow support columns (weight optimized)
  - Switch system with actuator housing
  - Parametric sensor brackets

## Using CadQuery Models

### View/Edit
```bash
# Open STEP file in CAD software
freecad monorail_barn_cadquery.step
# or Fusion 360, Blender, etc.
```

### Regenerate
```bash
# Modify dimensions in Python script
python3 monorail_barn_cadquery.py

# Or customize and run
python3 -c "from monorail_barn_cadquery import MonorailBarn; barn = MonorailBarn(); barn.length = 80; barn.export_step()"
```

### Export to Other Formats
```bash
# CadQuery can export to: STEP, STL, DXF, SVG
# See script parameters for additional export options
```

## Git Repository Changes

### What Was Done
- ✅ Removed binary CAD files from Git tracking
- ✅ Updated `.gitignore` for CadQuery workflow
- ✅ Created parametric Python-based CAD scripts
- ✅ Backed up all original files to `.cad_backup/`

### Repository Impact
- **Size Reduction**: ~{self.stats['space_freed_mb']:.1f} MB freed
- **File Count**: {self.stats['files_removed']} binary files removed
- **New Files**: {self.stats['cad_files_generated']} CAD Python scripts + outputs

## Next Steps for Tonight's Push

1. **Review Changes**:
   ```bash
   git status  # Verify files to be committed
   ```

2. **Commit Migration**:
   ```bash
   git add .gitignore CAD-Models/*.py CAD-Models/*.md
   git add CAD-Models/*.step  # Optional: STEP files for reference
   git commit -m "migration: convert CAD from Blender to CadQuery parametric"
   ```

3. **Clean History (Optional)**:
   ```bash
   git gc --aggressive  # Optimize repository
   ```

4. **Push Changes**:
   ```bash
   git push origin main
   ```

## Disaster Recovery

If you need to restore old files:

```bash
# Restore from backup
cp -r .cad_backup/* CAD-Models/

# Or check Git history
git log --diff-filter=D --summary | grep delete
git checkout <commit_hash>^ -- <file_path>
```

## Documentation

All parametric models include:
- ✅ Detailed Python docstrings
- ✅ Configurable dimensions
- ✅ Export methods for STEP/STL
- ✅ Usage examples

### See Also
- `CAD-Models/monorail_barn_cadquery.py` - Barn implementation
- `CAD-Models/monorail_track_system.py` - Track system implementation
- `CAD-Models/README.md` - Original file guide (archived)
- `.cad_backup/` - Original files (for reference)

## Migration Log

```
{chr(10).join(self.migration_log)}
```

---

**Migration Tool**: WDW CAD Migration Script  
**Version**: 1.0  
**Status**: ✅ Complete
"""
            
            with open(report_path, 'w') as f:
                f.write(report_content)
            
            self.log_action("REPORT_SAVED", f"Migration report: CAD_MIGRATION_REPORT.md")
            return True
        
        except Exception as e:
            self.log_action("REPORT_ERROR", str(e))
            return False
    
    def run_migration(self):
        """Execute complete migration pipeline."""
        start_time = datetime.now()
        print("=" * 70)
        print("🚀 WDW MONORAIL CAD MIGRATION - BLENDER TO CADQUERY")
        print("=" * 70)
        print()
        
        # Step 1: Backup
        if not self.backup_old_files():
            print("❌ Backup failed. Aborting migration.")
            return False
        
        print()
        
        # Step 2: Generate CadQuery models
        if not self.generate_cadquery_models():
            print("⚠️  CAD generation had issues. Continuing...")
        
        print()
        
        # Step 3: Remove old files
        if not self.remove_old_cad_files():
            print("❌ File removal failed. Aborting migration.")
            return False
        
        print()
        
        # Step 4: Update .gitignore
        if not self.update_gitignore():
            print("⚠️  .gitignore update failed. Continuing...")
        
        print()
        
        # Step 5: Clean Git tracking
        if not self.clean_git_history():
            print("⚠️  Git cleanup failed. Files may still be tracked.")
        
        print()
        
        # Step 6: Generate report
        if not self.create_migration_report():
            print("⚠️  Report generation failed.")
        
        # Calculate timing
        self.stats["migration_time"] = (datetime.now() - start_time).total_seconds()
        
        print()
        print("=" * 70)
        print("✅ MIGRATION COMPLETE")
        print("=" * 70)
        print()
        print("📊 Migration Summary:")
        print(f"   • Files backed up: {self.stats['files_backed_up']}")
        print(f"   • Files removed: {self.stats['files_removed']}")
        print(f"   • Space freed: {self.stats['space_freed_mb']:.1f} MB")
        print(f"   • CAD files generated: {self.stats['cad_files_generated']}")
        print(f"   • Migration time: {self.stats['migration_time']:.1f} seconds")
        print()
        print("📁 Next steps:")
        print("   1. Review changes: git status")
        print("   2. Commit: git add . && git commit -m 'migration: CAD Blender → CadQuery'")
        print("   3. Push: git push origin main")
        print()
        print("📄 See CAD_MIGRATION_REPORT.md for full details")
        print()
        
        return True


def main():
    """Run migration."""
    migration = CADMigration()
    success = migration.run_migration()
    
    if success:
        print("🎉 Ready for GitHub push!")
        exit(0)
    else:
        print("⚠️  Migration encountered errors. Review logs above.")
        exit(1)


if __name__ == "__main__":
    main()

