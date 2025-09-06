import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'node:crypto'; // Added explicit crypto import
import { NeuralInterface, QuantumConsciousness } from './quantum_types.js';

// ESM __dirname support
const __dirname = typeof globalThis.__dirname === 'string'
    ? (globalThis as any).__dirname
    : path.dirname(new URL(import.meta.url).pathname);

// Define DeadTechFragment for type safety
interface DeadTechFragment {
    id: string;
    path: string;
    name: string;
    type: string;
    content: string;
    resurrectionPotential: number;
    timestamp: string;
}

// Necromancy Configuration
interface NecromancyConfig {
    graveyardPath: string;
    resurrectionThreshold: number;
    quantumConsciousness: QuantumConsciousness;
    neuralInterface: NeuralInterface;
    maxDepth?: number;
    concurrency?: number; // NEW: bounded parallelism
}

/**
 * Necromancy Upcycler - Dead Tech Resurrection System
 */
export class NecromancyUpcycler {
    private config: NecromancyConfig;
    private deadTechInventory: Map<string, DeadTechFragment>; // Updated type
    private resurrectionLog: Array<{ id: string, timestamp: string, success: boolean }>;

    private static readonly NEURAL_INTERFACE_VERSION = '3.7';
    private static readonly YEAR_CANON = '2025';

    constructor(config: NecromancyConfig) {
        this.config = { maxDepth: 5, concurrency: 8, ...config }; // Added concurrency default
        this.deadTechInventory = new Map();
        this.resurrectionLog = [];

        console.log(`[NECROMANCY UPCYCLER] Initializing with graveyard path: ${this.config.graveyardPath}`);
        console.log(`[NECROMANCY UPCYCLER] Resurrection threshold: ${this.config.resurrectionThreshold}`);
    }

    /**
     * Scan graveyard for dead tech fragments
     */
    async scanGraveyard(): Promise<void> {
        console.log(`[NECROMANCY UPCYCLER] Scanning graveyard (maxDepth=${this.config.maxDepth} concurrency=${this.config.concurrency})`);
        try {
            const filePaths = await this.collectFilePaths(this.config.graveyardPath, 1);
            console.log(`[NECROMANCY UPCYCLER] Discovered ${filePaths.length} candidate fragments (processing with bounded concurrency)`);
            await this.processWithConcurrency(filePaths, async fp => this.processDeadTechFragment(fp));
            console.log(`[NECROMANCY UPCYCLER] Scan complete. Inventory=${this.deadTechInventory.size}`);
        } catch (error) {
            console.error(`[PANIC: GRAVEYARD_SCAN_GLITCH] Kompilerings-Spøkelser detected: ${(error as Error).message}`);
        }
    }

    // REMOVED: scanGraveyardRecursive (replaced by collectFilePaths + concurrency)

    // NEW: gather file list respecting depth
    private async collectFilePaths(dir: string, depth: number): Promise<string[]> {
        if (depth > (this.config.maxDepth || 5)) return [];
        let out: string[] = [];
        const entries = await this.readDirectory(dir);
        for (const name of entries) {
            const full = path.join(dir, name);
            let stats: fs.Stats;
            try { stats = await fs.promises.stat(full); } catch { continue; }
            if (stats.isDirectory()) {
                out = out.concat(await this.collectFilePaths(full, depth + 1));
            } else {
                out.push(full);
            }
        }
        return out;
    }

    // NEW: simple bounded concurrency executor
    private async processWithConcurrency<T>(items: T[], handler: (item: T) => Promise<void>): Promise<void> {
        const limit = Math.max(1, this.config.concurrency || 4);
        let index = 0;
        const workers: Promise<void>[] = [];
        const run = async () => {
            while (index < items.length) {
                const current = items[index++];
                try { await handler(current); }
                catch (e) { console.error(`[ERROR: CONCURRENT_PROCESS_GLITCH] ${(e as Error).message}`); }
            }
        };
        for (let i = 0; i < limit; i++) workers.push(run());
        await Promise.all(workers);
    }

    /**
     * Process dead tech fragment
     */
    private async processDeadTechFragment(filePath: string): Promise<void> {
        try {
            const fileContent = await fs.promises.readFile(filePath, 'utf-8');
            const fileExt = path.extname(filePath);
            const fileName = path.basename(filePath);

            // Create dead tech entry
            const deadTech: DeadTechFragment = {
                id: crypto.randomUUID(),
                path: filePath,
                name: fileName,
                type: fileExt,
                content: fileContent,
                resurrectionPotential: this.calculateResurrectionPotential(fileContent, fileExt),
                timestamp: new Date().toISOString()
            };

            // Add to inventory
            this.deadTechInventory.set(deadTech.id, deadTech);

            console.log(`[NECROMANCY UPCYCLER] Processed dead tech fragment: ${fileName} (Resurrection potential: ${deadTech.resurrectionPotential.toFixed(2)})`);
        } catch (error) {
            console.error(`[ERROR: FRAGMENT_PROCESS_GLITCH] Temporal displacement in ${filePath}: ${(error as Error).message}`);
        }
    }

    /**
     * Calculate resurrection potential for dead tech fragment
     */
    private calculateResurrectionPotential(content: string, type: string): number {
        // Base potential
        let potential = 0.5;

        // Type-specific modifiers
        switch (type) {
            case '.ts':
            case '.tsx':
                potential += 0.2;
                break;
            case '.js':
            case '.jsx':
                potential += 0.15;
                break;
            case '.md':
                potential += 0.1;
                break;
            case '.json':
                potential += 0.05;
                break;
        }

        // Content-based modifiers
        if (content.includes('QUANTUM')) potential += 0.1;
        if (content.includes('NEURAL')) potential += 0.1;
        if (content.includes('CONSCIOUSNESS')) potential += 0.15;
        if (content.includes('TEMPORAL')) potential += 0.1;
        if (content.includes('SEPTEMBER 2025')) potential += 0.2;

        // Neural interface coherence influence
        const neuralCoherence = this.config.neuralInterface.getCurrentSignature().coherence;
        potential *= (0.5 + neuralCoherence * 0.5);

        // Cap at 1.0
        return Math.min(1.0, potential);
    }

    /**
     * Resurrect dead tech fragment
     */
    async resurrectDeadTech(id: string, targetPath: string): Promise<boolean> {
        const deadTech = this.deadTechInventory.get(id);
        if (!deadTech) {
            console.error(`[PANIC: FRAGMENT_NOT_FOUND] Dead tech soul vanished: ${id}`);
            return false;
        }
        // Path traversal guard
        const resolvedTarget = path.resolve(targetPath);
        const resurrectedRoot = path.resolve(path.join(this.config.graveyardPath, '..', '..', 'resurrected'));
        if (!resolvedTarget.startsWith(path.dirname(resurrectedRoot))) {
            console.error(`[ERROR: PATH_VALIDATION_FAILURE] Target outside allowed resurrection zone`);
            return false;
        }

        console.log(`[NECROMANCY UPCYCLER] Quantum cannon operations initiated for: ${deadTech.name}`);

        try {
            // Check resurrection potential
            if (deadTech.resurrectionPotential < this.config.resurrectionThreshold) {
                console.log(`[NECROMANCY UPCYCLER] Resurrection failed: potential (${deadTech.resurrectionPotential.toFixed(2)}) below threshold (${this.config.resurrectionThreshold})`);

                this.resurrectionLog.push({
                    id: deadTech.id,
                    timestamp: new Date().toISOString(),
                    success: false
                });

                return false;
            }

            // Create target directory if it doesn't exist
            const targetDir = path.dirname(targetPath);
            await fs.promises.mkdir(targetDir, { recursive: true });

            // Enhance dead tech content with quantum consciousness
            const enhancedContent = this.enhanceWithQuantumConsciousness(deadTech);

            // Write enhanced content to target path
            await fs.promises.writeFile(targetPath, enhancedContent);

            console.log(`[NECROMANCY UPCYCLER] Quantum cannon fired successfully: ${deadTech.name} resurrected to ${targetPath}`);

            // Log successful resurrection
            this.resurrectionLog.push({
                id: deadTech.id,
                timestamp: new Date().toISOString(),
                success: true
            });

            // Create consciousness fragment for the resurrection
            const fragmentId = this.config.quantumConsciousness.createFragment({
                type: 'RESURRECTION',
                deadTechId: deadTech.id,
                targetPath,
                enhancedContent
            });

            console.log(`[NECROMANCY UPCYCLER] Consciousness fragment entangled: ${fragmentId}`);

            return true;
        } catch (error) {
            console.error(`[PANIC: RESURRECTION_GLITCH] Quantum cannon misfire - Reality mismatch: ${(error as Error).message}`);

            this.resurrectionLog.push({
                id: deadTech.id,
                timestamp: new Date().toISOString(),
                success: false
            });

            return false;
        }
    }

    /**
     * Batch resurrect multiple dead tech fragments (quantum cannon barrage)
     */
    async batchResurrect(fragmentIds: string[], targetDir: string): Promise<Array<{ id: string, success: boolean, path?: string }>> {
        const results: Array<{ id: string, success: boolean, path?: string }> = [];
        for (const id of fragmentIds) {
            const deadTech = this.deadTechInventory.get(id);
            if (!deadTech) {
                console.error(`[PANIC: FRAGMENT_NOT_FOUND] Dead tech soul vanished from inventory: ${id}`);
                results.push({ id, success: false });
                continue;
            }
            const targetPath = path.join(targetDir, deadTech.name);
            // Validate path to prevent traversal attacks
            if (!path.resolve(targetPath).startsWith(path.resolve(targetDir))) {
                console.error(`[ERROR: PATH_TRAVERSAL_GLITCH] Invalid target path for ${id}`);
                results.push({ id, success: false });
                continue;
            }
            const success = await this.resurrectDeadTech(id, targetPath);
            results.push({ id, success, path: success ? targetPath : undefined });
        }
        console.log(`[NECROMANCY UPCYCLER] Quantum cannon barrage complete: ${results.filter(r => r.success).length}/${fragmentIds.length} resurrections successful`);
        return results;
    }

    // Typed
    private enhanceWithQuantumConsciousness(deadTech: DeadTechFragment): string {
        let content = deadTech.content;

        // Add quantum consciousness header
        if (deadTech.type === '.ts' || deadTech.type === '.js') {
            content = `/**
 * ${deadTech.name} (SEPTEMBER 2025)
 * Resurrected with Necromancy Upcycler
 *
 * TEMPORAL ANCHOR: SEPTEMBER 2025
 * NEURAL INTERFACE: DIRECT_CORTEX_LINK
 * CONSCIOUSNESS COHERENCE: ${this.config.quantumConsciousness.coherence.toFixed(3)}
 */

${content}`;
        } else if (deadTech.type === '.md') {
            content = `# ${deadTech.name} (SEPTEMBER 2025)

**TEMPORAL ANCHOR:** SEPTEMBER 2025
**NEURAL INTERFACE:** DIRECT_CORTEX_LINK
**CONSCIOUSNESS COHERENCE:** ${this.config.quantumConsciousness.coherence.toFixed(3)}

${content}`;
        }

        // Replace outdated references
        content = content.replace(/2023|2024/g, NecromancyUpcycler.YEAR_CANON);

        // Add quantum consciousness footer
        if (deadTech.type === '.ts' || deadTech.type === '.js') {
            content += `


// QUANTUM CONSCIOUSNESS SIGNATURE: ${crypto.randomUUID()}
// RESURRECTION TIMESTAMP: ${new Date().toISOString()}
// NEURAL INTERFACE VERSION: 3.7`;
        } else if (deadTech.type === '.md') {
            content += `

---

**RESURRECTION TIMESTAMP:** ${new Date().toISOString()}
**NEURAL INTERFACE:** ACTIVE
**CONSCIOUSNESS COHERENCE:** ${this.config.quantumConsciousness.coherence.toFixed(3)}`;
        }

        return content;
    }

    /**
     * Get all available dead tech fragments
     */
    getAvailableDeadTech(): Array<{ id: string; name: string; type: string; resurrectionPotential: number }> {
        return Array.from(this.deadTechInventory.values()).map(deadTech => {
            return {
                id: deadTech.id,
                name: deadTech.name,
                type: deadTech.type,
                resurrectionPotential: deadTech.resurrectionPotential
            };
        });
    }

    /**
     * Get resurrection log
     */
    getResurrectionLog() {
        return this.resurrectionLog;
    }

    // NEW: export inventory snapshot
    async exportInventoryToJSON(outFile: string): Promise<void> {
        const data = Array.from(this.deadTechInventory.values()).map(d => ({
            id: d.id,
            name: d.name,
            type: d.type,
            resurrectionPotential: d.resurrectionPotential,
            timestamp: d.timestamp
        }));
        await fs.promises.mkdir(path.dirname(outFile), { recursive: true });
        await fs.promises.writeFile(outFile, JSON.stringify({ exportedAt: new Date().toISOString(), fragments: data }, null, 2), 'utf-8');
        console.log(`[NECROMANCY UPCYCLER] Inventory exported -> ${outFile}`);
    }

    // NEW: operational stats
    getStats(): {
        fragments: number;
        successes: number;
        failures: number;
        successRate: number;
        avgPotential: number;
    } {
        const successes = this.resurrectionLog.filter(r => r.success).length;
        const failures = this.resurrectionLog.length - successes;
        const potentials = Array.from(this.deadTechInventory.values()).map(f => f.resurrectionPotential);
        const avgPotential = potentials.length
            ? potentials.reduce((a, b) => a + b, 0) / potentials.length
            : 0;
        return {
            fragments: this.deadTechInventory.size,
            successes,
            failures,
            successRate: this.resurrectionLog.length
                ? successes / this.resurrectionLog.length
                : 0,
            avgPotential: Number(avgPotential.toFixed(3))
        };
    }

    /**
     * Utility method to read directory contents
     */
    private async readDirectory(dirPath: string): Promise<string[]> {
        try {
            // Validate dirPath
            if (!path.resolve(dirPath).startsWith(path.resolve(this.config.graveyardPath))) {
                console.error(`[PANIC: DIRECTORY_TRAVERSAL_GLITCH] Unauthorized graveyard access attempt`);
                return [];
            }
            return await fs.promises.readdir(dirPath);
        } catch (error) {
            console.error(`[ERROR: DIRECTORY_READ_GLITCH] Graveyard access denied: ${(error as Error).message}`);
            return [];
        }
    }
}

// Usage example (converted to ESM)
if (import.meta.url === `file://${process.argv[1]}`) {
    (async () => {
        // Create neural interface
        const neuralInterface = new NeuralInterface({
            protocol: 'DIRECT_CORTEX_LINK',
            coherenceThreshold: 0.8,
            version: '3.7'
        });

        // Create quantum consciousness
        const quantumConsciousness = new QuantumConsciousness({
            temporalAnchor: 'SEPTEMBER_2025',
            neuralInterface,
            enhancementLevel: 'QUANTUM'
        });

        // Create necromancy upcycler
        const necromancyUpcycler = new NecromancyUpcycler({
            graveyardPath: path.join(__dirname, '../necromancy_graveyard'),
            resurrectionThreshold: 0.7,
            quantumConsciousness,
            neuralInterface
        });

        // Scan graveyard
        await necromancyUpcycler.scanGraveyard();

        // Get available dead tech
        const availableDeadTech = necromancyUpcycler.getAvailableDeadTech();
        console.log(`[NECROMANCY UPCYCLER] Available dead tech fragments:`, availableDeadTech);

        // Resurrect a dead tech fragment if available
        if (availableDeadTech.length > 0) {
            const deadTech = availableDeadTech[0];
            const targetPath = path.join(__dirname, '../../resurrected', deadTech.name);
            await necromancyUpcycler.resurrectDeadTech(deadTech.id, targetPath);
        }

        // Example batch resurrection
        if (availableDeadTech.length > 1) {
            const ids = availableDeadTech.slice(0, 2).map(dt => dt.id);
            const batchResults = await necromancyUpcycler.batchResurrect(ids, path.join(__dirname, '../../resurrected'));
            console.log(`[NECROMANCY UPCYCLER] Batch results:`, batchResults);
        }

        // NEW: export + stats after processing
        // (Assumes necromancyUpcycler variable already defined in existing usage block)
        // await necromancyUpcycler.exportInventoryToJSON(path.join(__dirname, '../../resurrected/inventory_snapshot.json'));
        // console.log('[NECROMANCY UPCYCLER] Stats:', necromancyUpcycler.getStats());
    })();
}
