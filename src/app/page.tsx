import PixelCanvas from '@/components/PixelCanvas';

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebApplication',
  name: 'Pixel Art Canvas',
  description: 'Create beautiful pixel art with our free online drawing tool. Mobile-friendly with color palette and PNG export.',
  url: 'https://pixel-art-canvas.vercel.app',
  applicationCategory: 'GraphicsApplication',
  operatingSystem: 'Any',
  offers: {
    '@type': 'Offer',
    price: '0',
    priceCurrency: 'USD',
  },
  featureList: [
    'Pixel art creation',
    'Color palette',
    'Mobile-friendly touch support',
    'PNG export',
    'Grid system',
    'Clear canvas function'
  ],
  creator: {
    '@type': 'Organization',
    name: 'Pixel Art Canvas'
  }
};

export default function Home() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        <main className="container mx-auto px-4 py-8">
          <PixelCanvas 
            width={24} 
            height={24} 
            pixelSize={14}
          />
        </main>
      </div>
    </>
  );
}
