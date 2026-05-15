import { Component } from 'react'
import { Button, Result, Typography } from 'antd'

const { Paragraph, Text } = Typography

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error) {
    return { error }
  }

  componentDidUpdate(previousProps) {
    if (previousProps.resetKey !== this.props.resetKey && this.state.error) {
      this.setState({ error: null })
    }
  }

  render() {
    if (!this.state.error) return this.props.children

    return (
      <Result
        status="warning"
        title="页面渲染异常"
        subTitle="当前页面遇到本地渲染错误，mock 数据和后端服务不会因此被修改。"
        extra={
          <Button type="primary" onClick={this.props.onReset}>
            返回仪表盘
          </Button>
        }
      >
        <Paragraph>
          <Text type="secondary">{this.state.error?.message || 'Unknown frontend error'}</Text>
        </Paragraph>
      </Result>
    )
  }
}
