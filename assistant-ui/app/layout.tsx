'use client'

import "./globals.css";

import { cn } from "@/lib/utils";
import { Montserrat } from "next/font/google";
import { MyRuntimeProvider } from "@/components/MyRuntimeProvider";
import Script from 'next/script';

const montserrat = Montserrat({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <MyRuntimeProvider>
      <html lang="en">
        <head>
          <Script type="importmap" id="import-map-source" strategy="beforeInteractive">
            {`{
              "imports": {
                "@rhds/elements/": "https://cdn.jsdelivr.net/npm/@rhds/elements@2.1.1/elements/",
                "@rhds/icons/": "https://cdn.jsdelivr.net/npm/@rhds/icons@1.1.2/"
              },
              "scopes": {
                "https://cdn.jsdelivr.net/": {
                  "@floating-ui/core": "https://cdn.jsdelivr.net/npm/@floating-ui/core@1.6.8/dist/floating-ui.core.mjs",
                  "@floating-ui/dom": "https://cdn.jsdelivr.net/npm/@floating-ui/dom@1.6.12/dist/floating-ui.dom.mjs",
                  "@floating-ui/utils": "https://cdn.jsdelivr.net/npm/@floating-ui/utils@0.2.8/dist/floating-ui.utils.mjs",
                  "@floating-ui/utils/dom": "https://cdn.jsdelivr.net/npm/@floating-ui/utils@0.2.8/dist/floating-ui.utils.dom.mjs",
                  "@lit/context": "https://cdn.jsdelivr.net/npm/@lit/context@1.1.3/index.js",
                  "@lit/reactive-element": "https://cdn.jsdelivr.net/npm/@lit/reactive-element@2.0.4/reactive-element.js",
                  "@lit/reactive-element/decorators/": "https://cdn.jsdelivr.net/npm/@lit/reactive-element@2.0.4/decorators/",
                  "@patternfly/pfe-core": "https://cdn.jsdelivr.net/npm/@patternfly/pfe-core@4.0.4/core.js",
                  "@patternfly/pfe-core/": "https://cdn.jsdelivr.net/npm/@patternfly/pfe-core@4.0.4/",
                  "@patternfly/pfe-core/ssr-shims.js": "https://cdn.jsdelivr.net/npm/@patternfly/pfe-core@4.0.4/core.js",
                  "@rhds/elements/lib/": "https://cdn.jsdelivr.net/npm/@rhds/elements@2.1.1/lib/",
                  "@rhds/elements/": "https://cdn.jsdelivr.net/npm/@rhds/elements@2.1.1/elements/",
                  "@rhds/icons/ui/": "https://cdn.jsdelivr.net/npm/@rhds/icons@1.1.2/ui/",
                  "@rhds/tokens/css/": "https://cdn.jsdelivr.net/npm/@rhds/tokens@2.1.1/css/",
                  "@rhds/tokens/media.js": "https://cdn.jsdelivr.net/npm/@rhds/tokens@2.1.1/js/media.js",
                  "lit": "https://cdn.jsdelivr.net/npm/lit@3.2.1/index.js",
                  "lit-element/lit-element.js": "https://cdn.jsdelivr.net/npm/lit-element@4.1.1/lit-element.js",
                  "lit-html": "https://cdn.jsdelivr.net/npm/lit-html@3.2.1/lit-html.js",
                  "lit-html/": "https://cdn.jsdelivr.net/npm/lit-html@3.2.1/",
                  "lit/": "https://cdn.jsdelivr.net/npm/lit@3.2.1/",
                  "prism-esm": "https://cdn.jsdelivr.net/npm/prism-esm@1.29.0-fix.6/prism.js",
                  "prism-esm/components/": "https://cdn.jsdelivr.net/npm/prism-esm@1.29.0-fix.6/components/",
                  "tslib": "https://cdn.jsdelivr.net/npm/tslib@2.8.1/tslib.es6.mjs"
                }
              }
            }`}
          </Script>
        </head>

        <body className={cn(montserrat.className, "h-dvh")}>
          {children}
        </body>
      </html>
    </MyRuntimeProvider>
  );
}