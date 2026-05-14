export async function copyTextToClipboard(text) {
  if (!text) return false

  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text)
    return true
  }

  const textArea = document.createElement('textarea')
  textArea.value = text
  textArea.setAttribute('readonly', '')
  textArea.style.position = 'fixed'
  textArea.style.opacity = '0'
  document.body.appendChild(textArea)
  textArea.select()
  const copied = document.execCommand('copy')
  document.body.removeChild(textArea)
  return copied
}
