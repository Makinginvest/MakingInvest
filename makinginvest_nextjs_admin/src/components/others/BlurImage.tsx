import Image from 'next/image';
import { useState } from 'react';

export function BlurImage(props: any) {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className={`${props.className} overflow-hidden`}>
      <Image
        {...props}
        alt={props.alt}
        width={3840}
        height={2160}
        className={`next-img object-cover duration-500 transition-opacity ${
          isLoading ? 'grayscale blur-2xl scale-110' : 'grayscale-0 blur-0 scale-100'
        }`}
        onLoadingComplete={() => setIsLoading(false)}
      />
    </div>
  );
}
