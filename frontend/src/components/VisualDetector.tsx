import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { api } from '@/lib/api';
import { motion } from 'framer-motion';
import { 
  Upload, Loader2, AlertCircle, CheckCircle, 
  Image as ImageIcon, Eye, Brain, Layers, 
  FileText, Info, Target 
} from 'lucide-react';

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
      const response = await api.detectVisual(
        selectedFile,
        context.event || undefined,
        context.location || undefined,
        context.date || undefined
      );
      setResult(response);
      
      // Scroll to results after a brief delay
      setTimeout(() => {
        const resultsSection = document.getElementById('visual-results');
        if (resultsSection) {
          resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
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
              <motion.div
                id="visual-results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                {/* Header with Verdict */}
                {(() => {
                  const isAiGenerated = (result.ai_generated_score || 0) > 0.5;
                  const isManipulated = result.manipulation_detected;
                  const isSuspicious = isAiGenerated || isManipulated;
                  // fake_score is already 0-100, not 0-1
                  const fakeScore = result.final_verdict?.fake_score || 0;
                  
                  let verdictLabel = 'AUTHENTIC';
                  let verdictClass = 'bg-green-500';
                  
                  if (fakeScore >= 70) {
                    verdictLabel = 'SUSPICIOUS';
                    verdictClass = 'bg-red-500';
                  } else if (fakeScore >= 40) {
                    verdictLabel = 'QUESTIONABLE';
                    verdictClass = 'bg-yellow-500';
                  }
                  
                  return (
                    <Card className="border-2 border-blue-500 dark:border-blue-400">
                      <CardHeader className="pb-4">
                        <div className="flex items-center justify-between flex-wrap gap-4">
                          <CardTitle className="text-2xl">Visual Analysis Results</CardTitle>
                          <div className="flex items-center gap-4">
                            <Badge className={`${verdictClass} text-white text-base px-4 py-2`}>
                              {verdictLabel}
                            </Badge>
                            <span className="text-2xl font-bold">
                              {fakeScore.toFixed(1)}% Suspicious
                            </span>
                          </div>
                        </div>
                        {isSuspicious && (
                          <div className="flex items-start gap-2 mt-3 text-yellow-600 dark:text-yellow-400">
                            <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                            <span className="text-sm font-medium">Image authenticity questionable</span>
                          </div>
                        )}
                      </CardHeader>
                      
                      {isSuspicious && result.final_verdict?.reasons && (
                        <CardContent className="pt-0 pb-4 border-t border-slate-200 dark:border-slate-700">
                          <div className="space-y-3">
                            <div className="flex items-start gap-2 text-yellow-600 dark:text-yellow-400">
                              <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                              <div>
                                <div className="font-semibold">Recommendation:</div>
                                <div className="text-sm">Verify image authenticity - perform additional verification</div>
                              </div>
                            </div>
                            
                            <div>
                              <div className="font-semibold mb-2">Detection Reasons:</div>
                              <div className="space-y-1.5">
                                {result.final_verdict.reasons.map((reason: string, idx: number) => (
                                  <div key={idx} className="flex items-start gap-2 text-sm">
                                    <span className="text-red-500">-</span>
                                    <span>{reason}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        </CardContent>
                      )}
                    </Card>
                  );
                })()}
                
                {/* Detection Models Grid */}
                <div className="grid md:grid-cols-3 gap-4">
                  {/* Manipulation Check Card */}
                  {result.manipulation_check && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <Eye className="h-5 w-5 text-pink-500" />
                          <CardTitle className="text-base">Manipulation Check</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <Badge variant={result.manipulation_detected ? 'destructive' : 'success'}>
                          {result.manipulation_detected ? 'Manipulated' : 'Original'}
                        </Badge>
                        <div className="text-sm text-slate-600 dark:text-slate-400">
                          {result.manipulation_check.manipulation_probability !== undefined && (
                            <div>
                              {(result.manipulation_check.manipulation_probability > 1 
                                ? result.manipulation_check.manipulation_probability 
                                : result.manipulation_check.manipulation_probability * 100).toFixed(1)}% probability
                            </div>
                          )}
                          <div className="mt-1">Weight: 25%</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                  
                  {/* AI Generation Check Card */}
                  {result.ai_generation_check && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <Brain className="h-5 w-5 text-blue-500" />
                          <CardTitle className="text-base">AI Generation (CLIP)</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <Badge variant={result.ai_generation_check.is_ai_generated ? 'destructive' : 'success'}>
                          {result.ai_generation_check.is_ai_generated ? 'AI Generated' : 'Authentic'}
                        </Badge>
                        <div className="text-sm text-slate-600 dark:text-slate-400">
                          {result.ai_generation_check.likely_generator && (
                            <div className="font-medium">{result.ai_generation_check.likely_generator}</div>
                          )}
                          <div>
                            {(result.ai_generation_check.confidence > 1 
                              ? result.ai_generation_check.confidence 
                              : result.ai_generation_check.confidence * 100).toFixed(1)}% confidence
                          </div>
                          <div className="mt-1">Weight: 35%</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                  
                  {/* Image Content CNN Card */}
                  {result.cnn_prediction && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <Layers className="h-5 w-5 text-purple-500" />
                          <CardTitle className="text-base">Image Content (CNN)</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <Badge variant={result.cnn_prediction.is_fake ? 'destructive' : 'success'}>
                          {result.cnn_prediction.is_fake ? 'FAKE_CONTEXT' : 'REAL_CONTEXT'}
                        </Badge>
                        <div className="text-sm text-slate-600 dark:text-slate-400">
                          <div>CNN (547+2 image classifier)</div>
                          <div>
                            {(result.cnn_prediction.confidence > 1 
                              ? result.cnn_prediction.confidence 
                              : result.cnn_prediction.confidence * 100).toFixed(1)}% confidence
                          </div>
                          <div className="mt-1">Weight: 20%</div>
                          <div className="text-xs mt-1 text-slate-500">Trained on 100k images (95.7% accuracy)</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </div>
                
                {/* Context Verification & Content Analysis */}
                <div className="grid md:grid-cols-2 gap-4">
                  {/* Context Verification */}
                  {result.context_verification && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <CheckCircle className="h-5 w-5 text-green-500" />
                          <CardTitle className="text-base">Context Verification</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-sm">
                          <div className="font-medium mb-1">BLIP content analysis</div>
                          <div className="text-slate-600 dark:text-slate-400">Weight: 15%</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                  
                  {/* Content Analysis */}
                  {result.caption && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <FileText className="h-5 w-5 text-blue-500" />
                          <CardTitle className="text-base">Content Analysis</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-sm">
                          <div className="italic mb-2">"{result.caption}"</div>
                          <div className="text-slate-600 dark:text-slate-400">Local BLIP + OpenCV</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </div>
                
                {/* What's in the Image */}
                {(result.caption || result.description) && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader className="pb-3">
                      <div className="flex items-center gap-2">
                        <ImageIcon className="h-5 w-5 text-yellow-500" />
                        <CardTitle className="text-base">What's in the Image</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      {result.caption && (
                        <div className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800/50 rounded">
                          <span className="text-sm">{result.caption}</span>
                          <Badge variant="secondary">100%</Badge>
                        </div>
                      )}
                      
                      {result.description && result.description !== result.caption && (
                        <div className="p-3 bg-blue-50 dark:bg-blue-950/30 rounded border border-blue-200 dark:border-blue-800">
                          <div className="text-xs font-semibold text-blue-600 dark:text-blue-400 mb-1">
                            Detailed Description
                          </div>
                          <p className="text-sm text-slate-700 dark:text-slate-300">{result.description}</p>
                        </div>
                      )}
                      
                      {result.detected_objects && result.detected_objects.length > 0 && (
                        <div>
                          <div className="text-sm font-semibold mb-2">Objects Detected:</div>
                          <div className="flex flex-wrap gap-2">
                            {result.detected_objects.map((obj: any, idx: number) => (
                              <Badge key={idx} variant="outline">
                                {typeof obj === 'string' ? obj : obj.name} 
                                {obj.confidence && ` (${(obj.confidence > 1 ? obj.confidence : obj.confidence * 100).toFixed(0)}%)`}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {/* Google Vision Labels */}
                      {result.labels && result.labels.length > 0 && (
                        <div>
                          <div className="text-sm font-semibold mb-2">Google Vision Labels:</div>
                          <div className="flex flex-wrap gap-2">
                            {result.labels.map((label: any, idx: number) => {
                              const description = typeof label === 'string' ? label : (label.description || label.name);
                              const score = typeof label === 'object' && label.score 
                                ? (label.score > 1 ? label.score : label.score * 100).toFixed(0) 
                                : null;
                              
                              return (
                                <Badge key={idx} variant="outline" className="text-xs">
                                  {description}
                                  {score && <span className="ml-1 text-blue-600 dark:text-blue-400">({score}%)</span>}
                                </Badge>
                              );
                            })}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}
                
                {/* Face Analysis */}
                {result.faces_detected !== undefined && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader className="pb-3">
                      <div className="flex items-center gap-2">
                        <Eye className="h-5 w-5 text-orange-500" />
                        <CardTitle className="text-base">Face Analysis</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="text-sm">
                        Faces detected: <strong>{result.faces_detected}</strong>
                      </div>
                    </CardContent>
                  </Card>
                )}
                
                {/* Additional Analysis Details */}
                {(result.manipulation_check?.warning_signs || 
                  result.ai_generation_check?.details || 
                  result.context_verification?.analysis) && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base">Additional Analysis Details</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {result.manipulation_check?.warning_signs && 
                       result.manipulation_check.warning_signs.length > 0 && (
                        <div>
                          <div className="text-sm font-semibold mb-2 text-red-600 dark:text-red-400">
                            ⚠️ Manipulation Warning Signs:
                          </div>
                          <ul className="list-disc list-inside space-y-1">
                            {result.manipulation_check.warning_signs.map((sign: string, idx: number) => (
                              <li key={idx} className="text-sm text-slate-700 dark:text-slate-300">{sign}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {result.ai_generation_check?.details && (
                        <div>
                          <div className="text-sm font-semibold mb-2 text-blue-600 dark:text-blue-400">
                            🤖 AI Generation Details:
                          </div>
                          <p className="text-sm text-slate-700 dark:text-slate-300">
                            {result.ai_generation_check.details}
                          </p>
                        </div>
                      )}
                      
                      {result.context_verification?.analysis && (
                        <div>
                          <div className="text-sm font-semibold mb-2 text-purple-600 dark:text-purple-400">
                            📋 Context Verification:
                          </div>
                          <p className="text-sm text-slate-700 dark:text-slate-300">
                            {result.context_verification.analysis}
                          </p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}
                
                {/* Image Preview */}
                {preview && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader>
                      <CardTitle>Analyzed Image</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <img
                        src={preview}
                        alt="Analyzed"
                        className="max-w-full h-auto rounded-lg shadow-lg mx-auto"
                      />
                    </CardContent>
                  </Card>
                )}

                {/* Context Provided */}
                {(context.event || context.location || context.date) && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader className="pb-3">
                      <div className="flex items-center gap-2">
                        <Info className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                        <CardTitle className="text-base">Context Provided</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid md:grid-cols-3 gap-4 text-sm">
                        {context.event && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">Event</div>
                            <div className="font-medium">{context.event}</div>
                          </div>
                        )}
                        {context.location && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">Location</div>
                            <div className="font-medium">{context.location}</div>
                          </div>
                        )}
                        {context.date && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">Date</div>
                            <div className="font-medium">{context.date}</div>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Raw Data */}
                <Card className="border border-slate-300 dark:border-slate-700">
                  <CardContent className="pt-6">
                    <details className="cursor-pointer">
                      <summary className="font-medium text-slate-700 dark:text-slate-300 flex items-center gap-2">
                        <span>▶ View Raw Visual Analysis Data</span>
                      </summary>
                      <pre className="mt-4 p-4 bg-slate-50 dark:bg-slate-900 rounded-lg text-xs overflow-auto max-h-96 border border-slate-200 dark:border-slate-700">
                        {JSON.stringify(result, null, 2)}
                      </pre>
                    </details>
                  </CardContent>
                </Card>
              </motion.div>
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
