import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Catalog — Fabric catalog',
  description: 'Browse and filter all Fabric catalog solutions.',
};

export default function FabriccatalogLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}

