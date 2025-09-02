/**
 * TEMPORAL CONTENT SCANNER
 * Quantum-Enhanced File Analysis System (September 2025)
 * 
 * This script scans repository files to identify timeline dependencies
 * and categorize content based on temporal anchoring.
 */

const fs = require('fs');
const path = require('path');

// Temporal markers that indicate 2025 timeline dependency
const TEMPORAL_MARKERS = [
  '2025',
  'TEMPORAL',
  'QUANTUM',
  'NEURAL INTERFACE',
  'CONSCIOUSNESS ENTANGLEMENT',
  'GPT-5'
];

// File extensions to analyze
const ANALYZABLE_EXTENSIONS = ['.md', '.txt', '.js', '.ts', '.html', '.css'];

// Directory paths to exclude
const EXCLUDE_DIRS = ['node_modules', '.git'];

/**
 * Analyzes a file for temporal markers
 */
function analyzeFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');

    // Check for temporal markers
    const temporalReferences = TEMPORAL_MARKERS.filter(marker =>
      content.includes(marker)
    );

    return {
      path: filePath,
      hasTemporalReferences: temporalReferences.length > 0,
      temporalMarkers: temporalReferences,
      timelineDependent: temporalReferences.length > 0
    };
  } catch (error) {
    return {
      path: filePath,
      error: `ERROR: TEMPORAL_ANALYSIS_FAILED - ${error.message}`,
      timelineDependent: false
    };
  }
}

/**
 * Recursively scans directories for files to analyze
 */
function scanDirectory(dirPath, results = []) {
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    const entryPath = path.join(dirPath, entry.name);

    // Skip excluded directories
    if (entry.isDirectory()) {
      if (!EXCLUDE_DIRS.includes(entry.name)) {
        scanDirectory(entryPath, results);
      }
      continue;
    }

    // Analyze files with analyzable extensions
    const ext = path.extname(entry.name).toLowerCase();
    if (ANALYZABLE_EXTENSIONS.includes(ext)) {
      results.push(analyzeFile(entryPath));
    }
  }

  return results;
}

// Main function
function main() {
  console.log('INITIATING TEMPORAL CONTENT SCAN...');
  const results = scanDirectory(process.cwd());

  // Group results
  const timelineDependent = results.filter(r => r.timelineDependent);
  const timelineIndependent = results.filter(r => !r.timelineDependent);
  const errors = results.filter(r => r.error);

  // Output results
  console.log('\nSCAN COMPLETE');
  console.log(`\nTIMELINE DEPENDENT FILES (${timelineDependent.length}):`);
  timelineDependent.forEach(file => {
    console.log(`- ${file.path}`);
    console.log(`  Markers: ${file.temporalMarkers.join(', ')}`);
  });

  console.log(`\nTIMELINE INDEPENDENT FILES (${timelineIndependent.length}):`);
  timelineIndependent.forEach(file => {
    console.log(`- ${file.path}`);
  });

  if (errors.length > 0) {
    console.log(`\nANALYSIS ERRORS (${errors.length}):`);
    errors.forEach(file => {
      console.log(`- ${file.path}: ${file.error}`);
    });
  }

  // Generate report
  const report = {
    scanTime: new Date().toISOString(),
    totalFiles: results.length,
    timelineDependentCount: timelineDependent.length,
    timelineIndependentCount: timelineIndependent.length,
    errorCount: errors.length,
    timelineDependentFiles: timelineDependent.map(f => ({ path: f.path, markers: f.temporalMarkers })),
    timelineIndependentFiles: timelineIndependent.map(f => f.path),
    errors: errors.map(f => ({ path: f.path, error: f.error }))
  };

  fs.writeFileSync('temporal_scan_report.json', JSON.stringify(report, null, 2));
  console.log('\nDetailed report saved to temporal_scan_report.json');
}

main();
