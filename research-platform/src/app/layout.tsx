import type { Metadata } from 'next';
import './globals.css';
import { loadStepRegistry, loadPapers } from '@/lib/config';
import { AuditModeProvider } from '@/context/AuditModeContext';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { CommentComposer } from '@/components/audit/CommentComposer';

export const metadata: Metadata = {
  title: { default: 'Auditinsyt', template: '%s | Auditinsyt' },
  description: 'Auditinsyt is an evidence, artifact, and supervisor audit workspace for reproducible agricultural economics research.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const steps = loadStepRegistry();
  const papers = loadPapers();

  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css"
          integrity="sha384-GvrOXuhMATgEsSwCs4smwk74VEo54QRWBLolTH69Smpxke4YeqoMn4Hg3WiTrW56"
          crossOrigin="anonymous"
        />
      </head>
      <body>
        <AuditModeProvider>
          <div className="app-shell">
            <Sidebar steps={steps} papers={papers} />
            <div className="main-area">
              <Header />
              <main className="content">{children}</main>
            </div>
            <CommentComposer />
          </div>
        </AuditModeProvider>
      </body>
    </html>
  );
}
