import { useEffect, useState } from 'react'
import FileUpload from './components/FileUpload'
import TranscriptionViewer from './components/TranscriptionViewer'
import HistoryPanel from './components/HistoryPanel'

function App() {
  const [currentJob, setCurrentJob] = useState<any>(null)
  const [history, setHistory] = useState<any[]>([])

  useEffect(() => {
    // Load history on mount
    fetch('/api/v1/history')
      .then(res => res.json())
      .then(data => setHistory(data))
      .catch(() => {})
  }, [])

  const handleJobComplete = (job: any) => {
    setCurrentJob(job)
    setHistory(prev => [job, ...prev.filter(h => h.job_id !== job.job_id)])
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-primary-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="text-xl font-bold">Echo</div>
            </div>
            <div className="flex space-x-4">
              <a href="#" className="px-3 py-2 rounded-md text-sm font-medium">
                Home
              </a>
              <a href="#" className="px-3 py-2 rounded-md text-sm font-medium">
                History
              </a>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left column: File Upload */}
          <div className="lg:col-span-1">
            <FileUpload onJobComplete={handleJobComplete} />
            <div className="mt-8">
              <HistoryPanel history={history} />
            </div>
          </div>

          {/* Right column: Transcription Results */}
          <div className="lg:col-span-2">
            {currentJob ? (
              <TranscriptionViewer job={currentJob} />
            ) : (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <h3 className="text-lg font-medium text-gray-900">
                  No transcription yet
                </h3>
                <p className="mt-2 text-gray-500">
                  Upload an audio file to get started
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App