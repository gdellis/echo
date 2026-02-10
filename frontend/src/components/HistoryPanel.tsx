import { useState } from 'react'

interface Job {
  job_id: string
  filename: string
  status: string
  created_at: string
  duration: number
  speakers: number
}

interface HistoryPanelProps {
  history: Job[]
}

export default function HistoryPanel({ history }: HistoryPanelProps) {
  const [expandedJob, setExpandedJob] = useState<string | null>(null)

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const getStatusColor = (status: string) => {
    const colors = {
      queued: 'bg-gray-100 text-gray-800',
      processing: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">
          History
        </h3>
      </div>

      <div className="max-h-96 overflow-y-auto">
        {history.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            No transcription history yet
          </div>
        ) : (
          history.map((job) => (
            <div
              key={job.job_id}
              className="border-b border-gray-100 last:border-0"
            >
              <div
                className="px-6 py-4 cursor-pointer hover:bg-gray-50"
                onClick={() =>
                  setExpandedJob(expandedJob === job.job_id ? null : job.job_id)
                }
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {job.filename}
                    </p>
                    <p className="text-xs text-gray-500">
                      {new Date(job.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                        job.status
                      )}`}
                    >
                      {job.status}
                    </span>
                    <span className="text-xs text-gray-500">
                      {formatTime(job.duration)}
                    </span>
                  </div>
                </div>

                {expandedJob === job.job_id && (
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    <div className="flex items-center justify-between text-sm">
                      <div className="text-gray-600">
                        Speakers: {job.speakers}
                      </div>
                      <button className="text-primary-600 hover:text-primary-700">
                        View Details
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}