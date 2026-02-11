import { useState } from 'react'

interface Segment {
  start: number
  end: number
  text: string
  speaker: string
  confidence: number
}

interface Job {
  job_id: string
  status: string
  filename: string
  text: string
  segments: Segment[]
  speakers: number
  duration: number
}

interface TranscriptionViewerProps {
  job: Job
}

export default function TranscriptionViewer({ job }: TranscriptionViewerProps) {
  const [viewMode, setViewMode] = useState<'text' | 'json' | 'srt'>('text')

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const getSpeakerColor = (speaker: string) => {
    const colors = {
      'SPEAKER_00': 'bg-blue-100 text-blue-800 border-blue-200',
      'SPEAKER_01': 'bg-pink-100 text-pink-800 border-pink-200',
      'SPEAKER_02': 'bg-green-100 text-green-800 border-green-200',
      'SPEAKER_03': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'SPEAKER_04': 'bg-purple-100 text-purple-800 border-purple-200',
    }
    return colors[speaker as keyof typeof colors] || 'bg-gray-100 text-gray-800 border-gray-200'
  }

  const generateSRTContent = () => {
    return job.segments.reduce((acc, seg, index) => {
      const start = new Date(seg.start * 1000).toISOString().substr(11, 8).replace('.', ',')
      const end = new Date(seg.end * 1000).toISOString().substr(11, 8).replace('.', ',')
      return `${acc}${index + 1}\n${start} --> ${end}\n${seg.speaker}: ${seg.text}\n\n`
    }, '')
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              {job.filename}
            </h3>
            <p className="text-sm text-gray-500 mt-1">
              {job.speakers} speakers detected | {formatTime(job.duration)} duration
            </p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setViewMode('text')}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors
                ${viewMode === 'text' 
                  ? 'bg-primary-100 text-primary-700' 
                  : 'text-gray-600 hover:bg-gray-100'}`}
            >
              Text
            </button>
            <button
              onClick={() => setViewMode('srt')}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors
                ${viewMode === 'srt' 
                  ? 'bg-primary-100 text-primary-700' 
                  : 'text-gray-600 hover:bg-gray-100'}`}
            >
              SRT
            </button>
            <button
              onClick={() => setViewMode('json')}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors
                ${viewMode === 'json' 
                  ? 'bg-primary-100 text-primary-700' 
                  : 'text-gray-600 hover:bg-gray-100'}`}
            >
              JSON
            </button>
          </div>
        </div>
      </div>

      <div className="p-6">
        {viewMode === 'text' && (
          <div className="space-y-4">
            {job.segments.map((seg, idx) => (
              <div key={idx} className="flex gap-4">
                <div className="flex-shrink-0 w-20">
                  <span className="text-xs text-gray-500">
                    {formatTime(seg.start)} - {formatTime(seg.end)}
                  </span>
                </div>
                <div className="flex-grow">
                  <div className={`inline-block px-2 py-1 rounded text-sm font-medium mb-1 ${getSpeakerColor(seg.speaker)}`}>
                    {seg.speaker}
                  </div>
                  <p className="text-gray-700 leading-relaxed">{seg.text}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {viewMode === 'srt' && (
          <textarea
            className="w-full h-96 p-4 border rounded-md font-mono text-sm"
            readOnly
            value={generateSRTContent()}
          />
        )}

        {viewMode === 'json' && (
          <pre className="bg-gray-50 p-4 rounded-md overflow-auto max-h-96">
            <code className="text-sm">{JSON.stringify(job, null, 2)}</code>
          </pre>
        )}
      </div>

      <div className="border-t border-gray-200 px-6 py-4 bg-gray-50">
        <button className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors">
          Download {viewMode.toUpperCase()}
        </button>
      </div>
    </div>
  )
}