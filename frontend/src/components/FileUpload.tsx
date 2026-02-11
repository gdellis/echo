import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

const ACCEPTED_FILE_TYPES = {
  'audio/mpeg': ['.mp3'],
  'audio/wav': ['.wav'],
  'audio/x-m4a': ['.m4a'],
  'audio/mp4': ['.mp4', '.m4a'],
  'video/mp4': ['.mp4', '.mov'],
  'audio/flac': ['.flac'],
}

const MAX_FILE_SIZE = 500 * 1024 * 1024 // 500MB

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
  created_at?: string
}

interface FileUploadProps {
  onJobComplete: (job: Job) => void
}

export default function FileUpload({ onJobComplete }: FileUploadProps) {
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    
    if (file.size > MAX_FILE_SIZE) {
      alert('File too large. Maximum size is 500MB.')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/v1/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onJobComplete(response.data)
    } catch (error) {
      console.error('Error uploading file:', error)
      alert('Error uploading file. Please try again.')
    }
  }, [onJobComplete])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_FILE_TYPES,
    maxSize: MAX_FILE_SIZE,
  })

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">
        Upload Audio File
      </h3>
      
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-primary-500 bg-primary-50' 
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p className="text-primary-600 font-medium">
            Drop the file here
          </p>
        ) : (
          <div className="space-y-2">
            <p className="text-gray-700 font-medium">
              Drag and drop audio file here
            </p>
            <p className="text-sm text-gray-500">
              or click to browse
            </p>
            <p className="text-xs text-gray-400 mt-2">
              Supported: MP3, WAV, MP4, M4A, FLAC (max 500MB)
            </p>
          </div>
        )}
      </div>

      <div className="mt-4 space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Whisper Model
        </label>
        <select className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm">
          <option value="base">Base (default)</option>
          <option value="small">Small</option>
          <option value="medium">Medium</option>
          <option value="large">Large</option>
        </select>
      </div>

      <div className="mt-4">
        <label className="block text-sm font-medium text-gray-700">
          Language (optional)
        </label>
        <select className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm">
          <option value="">Auto-detect</option>
          <option value="en">English</option>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
          <option value="de">German</option>
          <option value="zh">Chinese</option>
          <option value="ja">Japanese</option>
          <option value="ko">Korean</option>
        </select>
      </div>
    </div>
  )
}