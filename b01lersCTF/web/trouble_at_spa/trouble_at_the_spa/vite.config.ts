import { defineConfig } from 'vite';

import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import obfuscator from 'vite-plugin-javascript-obfuscator';


export default defineConfig({
    plugins: [
        tailwindcss(),
        react(),
        obfuscator({  // Don't rev me :(
            options: {
                controlFlowFlattening: true,
                deadCodeInjection: true,
                debugProtection: true,
                numbersToExpressions: true,
                selfDefending: true,
                splitStrings: true,
                splitStringsChunkLength: 5,
                stringArrayCallsTransform: true,
                stringArrayEncoding: ["rc4"],
                stringArrayThreshold: 1,
                transformObjectKeys: true,
            }
        })
    ],
})
