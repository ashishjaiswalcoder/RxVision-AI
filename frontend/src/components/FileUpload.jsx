import { useState, useRef, useCallback } from 'react';
import { UploadCloud, X, Image as ImageIcon } from 'lucide-react';

const ACCEPT = '.jpeg,.jpg,.png,.webp';
const MAX_SIZE_MB = 10;

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function FileUpload({ file, onFileSelect, onRemove }) {
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef(null);
  const [preview, setPreview] = useState(null);

  const handleFile = useCallback(
    (f) => {
      if (!f) return;
      if (f.size > MAX_SIZE_MB * 1024 * 1024) {
        alert(`File too large. Maximum size is ${MAX_SIZE_MB}MB.`);
        return;
      }
      onFileSelect(f);
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(f);
    },
    [onFileSelect]
  );

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      setDragOver(false);
      const f = e.dataTransfer?.files?.[0];
      if (f) handleFile(f);
    },
    [handleFile]
  );

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => setDragOver(false);

  const handleChange = (e) => {
    const f = e.target.files?.[0];
    if (f) handleFile(f);
  };

  const handleRemove = (e) => {
    e.stopPropagation();
    onRemove();
    setPreview(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  const areaClass = [
    'upload-area',
    dragOver ? 'drag-over' : '',
    file ? 'has-file' : '',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div
      className={areaClass}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onClick={() => !file && inputRef.current?.click()}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          if (!file) inputRef.current?.click();
        }
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPT}
        onChange={handleChange}
        style={{ display: 'none' }}
      />

      {!file ? (
        <>
          <div className="upload-icon">
            <UploadCloud size={48} strokeWidth={1.5} />
          </div>
          <p className="upload-text">
            Drag & drop your prescription image here, or{' '}
            <strong>browse files</strong>
          </p>
          <p className="upload-hint">
            Supports JPEG, PNG, WebP · Max {MAX_SIZE_MB}MB
          </p>
        </>
      ) : (
        <div className="file-preview">
          {preview ? (
            <img
              className="file-preview-thumb"
              src={preview}
              alt="Preview"
            />
          ) : (
            <div
              className="file-preview-thumb flex items-center justify-center"
              style={{ background: 'rgba(255,255,255,0.03)' }}
            >
              <ImageIcon size={24} />
            </div>
          )}
          <div className="file-preview-info">
            <div className="file-preview-name">{file.name}</div>
            <div className="file-preview-size">{formatBytes(file.size)}</div>
          </div>
          <button
            className="btn-icon"
            onClick={handleRemove}
            aria-label="Remove file"
          >
            <X size={16} />
          </button>
        </div>
      )}
    </div>
  );
}
