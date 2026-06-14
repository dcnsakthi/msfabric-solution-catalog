import React from 'react';
import type { Metadata } from 'next';
import fs from 'fs';
import path from 'path';
import GettingStartedClient from './GettingStartedClient';

export const metadata: Metadata = {
  title: 'Getting Started — Fabric catalog',
  description: 'Learn how to install and use Fabric catalog for the first time.',
};

export default async function GettingStartedPage() {
  const contentPath = path.join(
    process.cwd(),
    'docs',
    'catalog',
    'getting-started',
    'content.md'
  );

  let content = '';
  if (fs.existsSync(contentPath)) {
    content = fs.readFileSync(contentPath, 'utf-8');
  }

  return <GettingStartedClient content={content} />;
}

