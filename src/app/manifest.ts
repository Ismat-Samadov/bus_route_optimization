import { MetadataRoute } from 'next'
 
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Pixel Art Canvas - Free Online Drawing Tool',
    short_name: 'Pixel Art Canvas',
    description: 'Create beautiful pixel art with our free online drawing tool. Mobile-friendly with color palette and PNG export.',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#3b82f6',
    categories: ['entertainment', 'productivity', 'graphics'],
    icons: [
      {
        src: '/icon-192x192.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icon-512x512.png',
        sizes: '512x512',
        type: 'image/png',
      },
    ],
  }
}