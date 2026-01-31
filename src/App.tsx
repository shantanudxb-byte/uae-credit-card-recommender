import { useState } from 'react'
import {
  AppLayout,
  TopNavigation,
  SideNavigation,
  ContentLayout,
  Header,
  Container,
  Grid,
  Box,
  Cards,
  Badge,
  Button,
  SpaceBetween,
  BarChart,
  LineChart
} from '@cloudscape-design/components'

function App() {
  const [activeHref, setActiveHref] = useState('/dashboard')

  const navigationItems = [
    { type: 'link', text: 'Dashboard', href: '/dashboard' },
    { type: 'link', text: 'Analytics', href: '/analytics' },
    { type: 'link', text: 'Users', href: '/users' },
    { type: 'link', text: 'Settings', href: '/settings' }
  ]

  const metrics = [
    { title: 'Total Users', value: '12,543', change: '+12%', status: 'positive' },
    { title: 'Revenue', value: '$45,231', change: '+8%', status: 'positive' },
    { title: 'Active Sessions', value: '1,234', change: '-3%', status: 'negative' },
    { title: 'Conversion Rate', value: '3.2%', change: '+0.5%', status: 'positive' },
    { title: 'Payment Success Rate', value: '98.5%', change: '+1%', status: 'positive' }
  ]

  const chartData = [
    { x: 'Jan', y: 120 },
    { x: 'Feb', y: 150 },
    { x: 'Mar', y: 180 },
    { x: 'Apr', y: 200 },
    { x: 'May', y: 240 },
    { x: 'Jun', y: 280 }
  ]

  return (
    <>
      <TopNavigation
        identity={{
          href: '/',
          title: 'SaaS Dashboard'
        }}
        utilities={[
          {
            type: 'button',
            text: 'Profile',
            href: '/profile'
          }
        ]}
      />
      <AppLayout
        navigation={
          <SideNavigation
            activeHref={activeHref}
            onFollow={(event) => {
              if (!event.detail.external) {
                event.preventDefault()
                setActiveHref(event.detail.href)
              }
            }}
            items={navigationItems}
          />
        }
        content={
          <ContentLayout
            header={
              <Header
                variant="h1"
                description="Monitor your application performance and user engagement"
                actions={
                  <SpaceBetween direction="horizontal" size="xs">
                    <Button>Export Data</Button>
                    <Button variant="primary">Refresh</Button>
                  </SpaceBetween>
                }
              >
                Dashboard Overview
              </Header>
            }
          >
            <SpaceBetween size="l">
              <Grid
                gridDefinition={[
                  { colspan: { default: 12, xs: 6, s: 3 } },
                  { colspan: { default: 12, xs: 6, s: 3 } },
                  { colspan: { default: 12, xs: 6, s: 3 } },
                  { colspan: { default: 12, xs: 6, s: 3 } },
                  { colspan: { default: 12, xs: 6, s: 3 } }
                ]}
              >
                {metrics.map((metric, index) => (
                  <Container key={index}>
                    <Box padding="m">
                      <SpaceBetween size="xs">
                        <Box variant="awsui-key-label">{metric.title}</Box>
                        <Box fontSize="display-l" fontWeight="bold">
                          {metric.value}
                        </Box>
                        <Badge color={metric.status === 'positive' ? 'green' : 'red'}>
                          {metric.change}
                        </Badge>
                      </SpaceBetween>
                    </Box>
                  </Container>
                ))}
              </Grid>

              <Grid
                gridDefinition={[
                  { colspan: { default: 12, s: 8 } },
                  { colspan: { default: 12, s: 4 } }
                ]}
              >
                <Container
                  header={
                    <Header variant="h2">
                      Monthly Growth
                    </Header>
                  }
                >
                  <LineChart
                    series={[
                      {
                        title: 'Users',
                        type: 'line',
                        data: chartData
                      }
                    ]}
                    xDomain={chartData.map(d => d.x)}
                    yDomain={[0, 300]}
                    i18nStrings={{
                      filterLabel: 'Filter displayed data',
                      filterPlaceholder: 'Filter data',
                      filterSelectedAriaLabel: 'selected',
                      legendAriaLabel: 'Legend',
                      chartAriaRoleDescription: 'line chart'
                    }}
                    ariaLabel="Monthly user growth chart"
                    height={300}
                  />
                </Container>

                <Container
                  header={
                    <Header variant="h2">
                      Recent Activity
                    </Header>
                  }
                >
                  <SpaceBetween size="m">
                    <Box>
                      <SpaceBetween size="xs">
                        <Box variant="strong">New user registration</Box>
                        <Box variant="small" color="text-body-secondary">2 minutes ago</Box>
                      </SpaceBetween>
                    </Box>
                    <Box>
                      <SpaceBetween size="xs">
                        <Box variant="strong">Payment processed</Box>
                        <Box variant="small" color="text-body-secondary">5 minutes ago</Box>
                      </SpaceBetween>
                    </Box>
                    <Box>
                      <SpaceBetween size="xs">
                        <Box variant="strong">System backup completed</Box>
                        <Box variant="small" color="text-body-secondary">1 hour ago</Box>
                      </SpaceBetween>
                    </Box>
                  </SpaceBetween>
                </Container>
              </Grid>
            </SpaceBetween>
          </ContentLayout>
        }
        toolsHide
      />
    </>
  )
}

export default App