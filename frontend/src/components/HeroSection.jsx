import { useEffect, useRef } from 'react';
import HeroNavbar from './HeroNavbar';
import LogoMarquee from './LogoMarquee';

const VIDEO_URL =
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_065045_c44942da-53c6-4804-b734-f9e07fc22e08.mp4';

export default function HeroSection() {
  const videoRef = useRef(null);
  const rafRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handlePlay = () => {
      const startTime = performance.now();
      const fadeIn = (now) => {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / 500, 1);
        video.style.opacity = progress;
        if (progress < 1) {
          rafRef.current = requestAnimationFrame(fadeIn);
        }
      };
      rafRef.current = requestAnimationFrame(fadeIn);
    };

    const handleTimeUpdate = () => {
      if (!video.duration) return;
      const remaining = video.duration - video.currentTime;
      if (remaining <= 0.5) {
        const progress = remaining / 0.5;
        video.style.opacity = Math.max(progress, 0);
      }
    };

    const handleEnded = () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      video.style.opacity = 0;
      setTimeout(() => {
        video.currentTime = 0;
        video.play().catch(() => {});
      }, 100);
    };

    video.addEventListener('play', handlePlay);
    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('ended', handleEnded);

    video.play().catch(() => {});

    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('ended', handleEnded);
    };
  }, []);

  return (
    <section className="hero-section">
      {/* Background Video */}
      <div className="hero-video-wrapper">
        <video
          ref={videoRef}
          className="hero-video"
          src={VIDEO_URL}
          muted
          playsInline
          preload="auto"
          style={{ opacity: 0 }}
        />
      </div>

      {/* Content Layer */}
      <div className="hero-content-layer">
        {/* Navbar */}
        <HeroNavbar />

        {/* Blurred overlay shape */}
        <div className="hero-blur-shape" />

        {/* Hero Content */}
        <div className="hero-center">
          <div className="hero-center-inner">
            <h1 className="hero-headline">
              <span className="hero-headline-plain">Rx</span>
              <span className="hero-headline-gradient">Vision</span>
            </h1>

            <p className="hero-subtitle-new">
              AI-powered prescription reader that decodes<br />
              handwritten prescriptions instantly
            </p>

            <a href="#app-content" className="hero-cta-btn">
              Upload Prescription
            </a>
          </div>
        </div>

        {/* Logo Marquee */}
        <div className="hero-marquee-wrapper">
          <LogoMarquee />
        </div>
      </div>
    </section>
  );
}
