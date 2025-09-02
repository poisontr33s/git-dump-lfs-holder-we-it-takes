#!/usr/bin/env bun
// 🎨 Export All District Visualizations
import { VisualMILFDistrictGenerator } from './hooks/visual_milf_district_generator.ts';

const generator = new VisualMILFDistrictGenerator();
await generator.export_all_district_packages('./district_visuals');

console.log('✅ All district visualizations exported to ./district_visuals/');
