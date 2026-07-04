const techs = [
  { name: 'Tesseract', letter: 'T' },
  { name: 'EasyOCR', letter: 'E' },
  { name: 'Google Vision', letter: 'G' },
  { name: 'React', letter: 'R' },
  { name: 'FastAPI', letter: 'F' },
  { name: 'Vite', letter: 'V' },
];

function TechLogo({ name, letter }) {
  return (
    <div className="marquee-logo-item">
      <div className="liquid-glass marquee-logo-icon">
        <span>{letter}</span>
      </div>
      <span className="marquee-logo-name">{name}</span>
    </div>
  );
}

export default function LogoMarquee() {
  return (
    <div className="marquee-container">
      {/* Left: Static text */}
      <div className="marquee-label">
        <span>Powered by cutting-edge</span>
        <span>AI & OCR technology</span>
      </div>

      {/* Right: Scrolling marquee */}
      <div className="marquee-track-wrapper">
        <div className="marquee-track">
          {/* First set */}
          {techs.map((tech) => (
            <TechLogo key={`a-${tech.name}`} {...tech} />
          ))}
          {/* Duplicate for seamless loop */}
          {techs.map((tech) => (
            <TechLogo key={`b-${tech.name}`} {...tech} />
          ))}
        </div>
      </div>
    </div>
  );
}
