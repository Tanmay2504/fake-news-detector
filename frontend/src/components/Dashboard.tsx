import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Shield, 
  Brain, 
  Eye, 
  Zap, 
  Target,
  BarChart3,
  FileText,
  Image as ImageIcon,
  AlertTriangle,
  CheckCircle2,
  TrendingUp,
  Clock
} from 'lucide-react';
import { api } from '@/lib/api';

interface DashboardProps {
  onStartDetection: () => void;
  onStartVisual: () => void;
}

export function Dashboard({ onStartDetection, onStartVisual }: DashboardProps) {
  const [health, setHealth] = useState<any>(null);
  const [stats] = useState({
    textAnalyzed: 15234,
    imagesScanned: 4521,
    fakeDetected: 8912,
    accuracy: 90.94
  });

  useEffect(() => {
    api.health().then(setHealth).catch(console.error);
  }, []);

  const features = [
    {
      icon: Brain,
      title: 'Ensemble ML',
      description: 'Random Forest (60%) + LightGBM (20%) + XGBoost (20%)',
      color: 'text-blue-600 dark:text-blue-400'
    },
    {
      icon: Eye,
      title: 'Visual Detection',
      description: 'AI-generated image detection & manipulation analysis',
      color: 'text-purple-600 dark:text-purple-400'
    },
    {
      icon: Target,
      title: 'Rule-Based Patterns',
      description: 'Fake/real news linguistic indicators',
      color: 'text-green-600 dark:text-green-400'
    },
    {
      icon: Zap,
      title: 'LIME Explainability',
      description: 'Word-level prediction explanations',
      color: 'text-orange-600 dark:text-orange-400'
    }
  ];

  const exampleTexts = [
    {
      text: "BREAKING!!! SHOCKING discovery about vaccines that THEY don't want you to know!!!",
      label: 'Likely Fake',
      confidence: 94.2,
      type: 'fake'
    },
    {
      text: "The Senate passed the infrastructure bill with bipartisan support according to Reuters.",
      label: 'Likely Real',
      confidence: 87.5,
      type: 'real'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100 dark:from-slate-950 dark:via-blue-950 dark:to-slate-900">
      <div className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="flex items-center justify-center gap-3 mb-6">
            <Shield className="h-16 w-16 text-blue-600 dark:text-blue-400" />
            <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400">
              Fake News Detector
            </h1>
          </div>
          <p className="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto mb-4">
            Advanced AI-powered system using ensemble machine learning and visual analysis to detect misinformation
          </p>
          <div className="flex items-center justify-center gap-4 flex-wrap">
            <Badge variant="success" className="text-sm px-4 py-1">
              <CheckCircle2 className="h-4 w-4 mr-1" />
              {stats.accuracy}% Accuracy
            </Badge>
            <Badge variant="secondary" className="text-sm px-4 py-1">
              <TrendingUp className="h-4 w-4 mr-1" />
              {stats.textAnalyzed.toLocaleString()} Analyzed
            </Badge>
            {health?.ok && (
              <Badge variant="success" className="text-sm px-4 py-1">
                <Zap className="h-4 w-4 mr-1" />
                {health.models_available.length} Models Active
              </Badge>
            )}
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid md:grid-cols-2 gap-6 mb-16"
        >
          <Card className="hover:shadow-xl transition-shadow cursor-pointer group border-2 hover:border-blue-500 dark:hover:border-blue-400" onClick={onStartDetection}>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg group-hover:scale-110 transition-transform">
                  <FileText className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <CardTitle className="text-2xl">Text Analysis</CardTitle>
                  <CardDescription>Analyze news articles for authenticity</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  Ensemble ML prediction
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  Rule-based pattern analysis
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  LIME explainability
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card className="hover:shadow-xl transition-shadow cursor-pointer group border-2 hover:border-purple-500 dark:hover:border-purple-400" onClick={onStartVisual}>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-lg group-hover:scale-110 transition-transform">
                  <ImageIcon className="h-8 w-8 text-purple-600 dark:text-purple-400" />
                </div>
                <div>
                  <CardTitle className="text-2xl">Visual Detection</CardTitle>
                  <CardDescription>Detect manipulated and AI-generated images</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  AI-generated detection
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  Manipulation analysis
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  Google Vision labels
                </li>
              </ul>
            </CardContent>
          </Card>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-center mb-8 text-slate-900 dark:text-slate-100">
            Powerful Features
          </h2>
          <div className="grid md:grid-cols-4 gap-6">
            {features.map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + idx * 0.1 }}
              >
                <Card className="h-full hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <feature.icon className={`h-10 w-10 ${feature.color} mb-2`} />
                    <CardTitle className="text-lg">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      {feature.description}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Example Predictions */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <h2 className="text-3xl font-bold text-center mb-8 text-slate-900 dark:text-slate-100">
            See It In Action
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {exampleTexts.map((example, idx) => (
              <Card key={idx} className={`border-2 ${example.type === 'fake' ? 'border-red-200 dark:border-red-800' : 'border-green-200 dark:border-green-800'}`}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <Badge variant={example.type === 'fake' ? 'destructive' : 'success'}>
                      {example.label}
                    </Badge>
                    <span className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                      {example.confidence}% confidence
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-slate-700 dark:text-slate-300 italic">
                    "{example.text}"
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </motion.div>

        {/* Stats Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="mt-16 grid md:grid-cols-4 gap-6"
        >
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Articles Analyzed</CardDescription>
              <CardTitle className="text-3xl">{stats.textAnalyzed.toLocaleString()}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Images Scanned</CardDescription>
              <CardTitle className="text-3xl">{stats.imagesScanned.toLocaleString()}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Fake News Detected</CardDescription>
              <CardTitle className="text-3xl text-red-600">{stats.fakeDetected.toLocaleString()}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Model Accuracy</CardDescription>
              <CardTitle className="text-3xl text-green-600">{stats.accuracy}%</CardTitle>
            </CardHeader>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
