import { useState } from 'react'

function App() {
  const [inputText, setInputText] = useState('')
  const [translation, setTranslation] = useState('')
  const [keywords, setKeywords] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleTranslate = async () => {
    if (!inputText.trim()) {
      setError('请输入要翻译的中文内容')
      return
    }

    setLoading(true)
    setError('')
    setTranslation('')
    setKeywords([])

    try {
      const response = await fetch('http://localhost:8000/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || '翻译请求失败')
      }

      const data = await response.json()
      setTranslation(data.translation)
      setKeywords(data.keywords || [])
    } catch (err) {
      setError(err.message || '翻译服务暂时不可用，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleTranslate()
    }
  }

  return (
    <div className="app">
      {/* 背景装饰 */}
      <div className="bg-decoration">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="blob blob-3"></div>
      </div>

      <div className="container">
        {/* 头部 */}
        <header className="header">
          <div className="logo">
            <span className="logo-icon">译</span>
            <h1>AI翻译助手</h1>
          </div>
          <p className="subtitle">智能中英翻译 · 关键词提取</p>
        </header>

        {/* 主内容区 */}
        <main className="main">
          {/* 输入区域 */}
          <section className="input-section">
            <div className="section-header">
              <span className="section-icon">📝</span>
              <h2>输入中文</h2>
            </div>
            <textarea
              className="input-textarea"
              placeholder="请输入要翻译的中文内容...&#10;&#10;提示：按 Ctrl+Enter 快速翻译"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              maxLength={5000}
            />
            <div className="input-footer">
              <span className="char-count">{inputText.length} / 5000</span>
              <button 
                className={`translate-btn ${loading ? 'loading' : ''}`}
                onClick={handleTranslate}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    翻译中...
                  </>
                ) : (
                  '开始翻译'
                )}
              </button>
            </div>
          </section>

          {/* 错误提示 */}
          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          {/* 结果区域 */}
          {(translation || keywords.length > 0) && (
            <section className="result-section">
              {/* 翻译结果 */}
              <div className="result-block translation-block">
                <div className="section-header">
                  <span className="section-icon">🌐</span>
                  <h2>英文翻译</h2>
                </div>
                <div className="result-content">
                  {translation || '翻译结果将显示在这里'}
                </div>
                <button 
                  className="copy-btn"
                  onClick={() => {
                    navigator.clipboard.writeText(translation)
                    alert('已复制到剪贴板！')
                  }}
                >
                  📋 复制
                </button>
              </div>

              {/* 关键词 */}
              {keywords.length > 0 && (
                <div className="result-block keywords-block">
                  <div className="section-header">
                    <span className="section-icon">🏷️</span>
                    <h2>关键词</h2>
                  </div>
                  <div className="keywords-list">
                    {keywords.map((keyword, index) => (
                      <span key={index} className="keyword-tag">
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </section>
          )}
        </main>

        {/* 页脚 */}
        <footer className="footer">
          <p>Powered by DeepSeek AI </p>
        </footer>
      </div>
    </div>
  )
}

export default App

