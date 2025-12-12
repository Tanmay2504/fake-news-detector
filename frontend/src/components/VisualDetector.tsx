import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { api } from '@/lib/api';
import { motion } from 'framer-motion';
import { Upload, Loader2, AlertCircle, CheckCircle, Image as ImageIcon } from 'lucide-react';

export function VisualDetector() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [context, setContext] = useState({
    event: '',
    location: '',
    date: '',
  });
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      setResult(null);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await api.detectVisual(selectedFile, {
        event: context.event || undefined,
        location: context.location || undefined,
        date: context.date || undefined,
      });
      setResult(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900 py-12 px-4">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-600 dark:from-white dark:to-slate-300">
            Visual Fake News Detector
          </h1>
          <p className="text-slate-600 dark:text-slate-400 text-lg">
            AI-powered image manipulation and deepfake detection
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Upload Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8"
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-200 mb-2">
                  Upload Image
                </label>
                <div
                  onClick={() => fileInputRef.current?.click()}
                  className="border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 dark:hover:border-blue-400 transition-colors"
                >
                  {preview ? (
                    <div className="space-y-4">
                      <img
                        src={preview}
                        alt="Preview"
                        className="max-h-64 mx-auto rounded-lg shadow-lg"
                      />
                      <p className="text-sm text-slate-600 dark:text-slate-400">
                        {selectedFile?.name}
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <Upload className="h-16 w-16 mx-auto text-slate-400" />
                      <div>
                        <p className="text-slate-700 dark:text-slate-300 font-medium">
                          Click to upload image
                        </p>
                        <p className="text-sm text-slate-500 dark:text-slate-400">
                          PNG, JPG, JPEG up to 10MB
                        </p>
                      </div>
                    </div>
                  )}
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </div>

              <div className="space-y-4">
                <h3 className="font-semibold text-slate-700 dark:text-slate-200">
                  Context (Optional)
                </h3>
                <Input
                  placeholder="Event (e.g., Election Rally)"
                  value={context.event}
                  onChange={(e) => setContext({ ...context, event: e.target.value })}
                  disabled={loading}
                />
                <Input
                  placeholder="Location (e.g., New York)"
                  value={context.location}
                  onChange={(e) => setContext({ ...context, location: e.target.value })}
                  disabled={loading}
                />
                <Input
                  placeholder="Date (e.g., 2024-01-15)"
                  value={context.date}
                  onChange={(e) => setContext({ ...context, date: e.target.value })}
                  disabled={loading}
                />
              </div>

              <Button
                type="submit"
                disabled={loading || !selectedFile}
                className="w-full h-12 text-lg"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <ImageIcon className="mr-2 h-5 w-5" />
                    Analyze Image
                  </>
                )}
              </Button>
            </form>
          </motion.div>

          {/* Results Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="space-y-6"
          >
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
                <div className="flex items-start">
                  <AlertCircle className="h-6 w-6 text-red-600 dark:text-red-400 mr-3 flex-shrink-0 mt-0.5" />
                  <div>
                    <h3 className="font-semibold text-red-900 dark:text-red-100 mb-1">Error</h3>
                    <p className="text-red-700 dark:text-red-300">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {result && (
              <div className="space-y-6">
                {/* Overall Assessment */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <CheckCircle className="h-6 w-6 mr-2 text-green-600 dark:text-green-400" />
                      Analysis Complete
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {result.manipulation_detected !== undefined && (
                      <div className="flex justify-between items-center">
                        <span className="text-slate-700 dark:text-slate-300">Manipulation Detected</span>
                        <Badge variant={result.manipulation_detected ? 'destructive' : 'success'}>
                          {result.manipulation_detected ? 'Yes' : 'No'}
                        </Badge>
                      </div>
                    )}
                    {result.ai_generated_score !== undefined && (
                      <div className="flex justify-between items-center">
                        <span className="text-slate-700 dark:text-slate-300">AI Generated Score</span>
                        <Badge variant="secondary">
                          {(result.ai_generated_score * 100).toFixed(1)}%
                        </Badge>
                      </div>
                    )}
                    {result.confidence !== undefined && (
                      <div className="flex justify-between items-center">
                        <span className="text-slate-700 dark:text-slate-300">Confidence</span>
                        <Badge variant="secondary">
                          {(result.confidence * 100).toFixed(1)}%
                        </Badge>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Labels */}
                {result.labels && result.labels.length > 0 && (
                  <Card>
                    <CardHeader>
                      <CardTitle>Detected Labels</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="flex flex-wrap gap-2">
                        {result.labels.slice(0, 10).map((label: any, idx: number) => (
                          <Badge key={idx} variant="outline">
                            {typeof label === 'string' ? label : label.description || label.name}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Additional Details */}
                {result.description && (
                  <Card>
                    <CardHeader>
                      <CardTitle>Description</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-slate-700 dark:text-slate-300">{result.description}</p>
                    </CardContent>
                  </Card>
                )}

                {/* Raw Result for Debugging */}
                <details className="bg-slate-100 dark:bg-slate-800/50 rounded-lg p-4">
                  <summary className="cursor-pointer font-medium text-slate-700 dark:text-slate-300">
                    View Raw Result
                  </summary>
                  <pre className="mt-3 text-xs text-slate-600 dark:text-slate-400 overflow-auto">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </details>
              </div>
            )}

            {!result && !error && (
              <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-12 text-center">
                <ImageIcon className="h-16 w-16 mx-auto text-slate-300 dark:text-slate-600 mb-4" />
                <p className="text-slate-500 dark:text-slate-400">
                  Upload an image to see analysis results
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
