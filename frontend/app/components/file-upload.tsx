"use client";

import { useCallback, useState } from "react";

import { Upload, FileText, X } from "lucide-react";

import { Button } from "~/components/ui/button";

type props = {
  /**
   * xml ファイル
   */
  file: File | null;
  /**
   * ファイル変更時に発火する関数
   */
  onFileChange: (file: File | null) => void;
};

export const FileUpload = ({ file, onFileChange }: props) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setIsDragging(false);
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile) {
        onFileChange(droppedFile);
      }
    },
    [onFileChange]
  );

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = e.target.files?.[0];
      if (selectedFile) {
        onFileChange(selectedFile);
      }
    },
    [onFileChange]
  );

  return (
    <div className="flex flex-col gap-3">
      <p className="cursor-pointer text-xs text-muted-foreground duration-100 hover:underline">
        iPhone 端末以外の方について
      </p>

      {!file ? (
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          className={`
            relative flex flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed px-6 py-10
            transition-colors
            ${
              isDragging
                ? "border-primary bg-primary/5"
                : "border-border bg-card hover:border-primary/50"
            }`}
        >
          <Upload className="h-8 w-8 text-muted-foreground" />
          <div className="text-center">
            <p className="text-sm text-foreground">ドラッグ&ドロップ、または</p>
            <label
              htmlFor="file-input"
              className={`
                cursor-pointer text-sm font-medium text-primary underline underline-offset-2
                hover:text-primary/80
              `}
            >
              ファイルを選択
            </label>
          </div>
          <p className="text-xs text-muted-foreground">XML ファイル</p>
          <input
            id="file-input"
            type="file"
            accept=".xml"
            onChange={handleFileSelect}
            className="sr-only"
          />
        </div>
      ) : (
        <div className="flex items-center gap-3 rounded-lg border border-border bg-card px-4 py-3">
          <FileText className="h-5 w-5 shrink-0 text-primary" />
          <div className="flex min-w-0 flex-1 flex-col">
            <p className="truncate text-sm font-medium text-foreground">
              {file.name}
            </p>
            <p className="text-xs text-muted-foreground">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onFileChange(null)}
            className="h-8 w-8 shrink-0 text-muted-foreground hover:text-foreground"
            aria-label="ファイルを削除"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      )}
    </div>
  );
};
