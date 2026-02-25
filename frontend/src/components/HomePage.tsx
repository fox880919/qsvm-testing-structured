import { useSiteCopy } from '../SiteCopyContext'
import { EditableText } from './EditableText'

export function HomePage() {
  const { siteCopy } = useSiteCopy()
  const { project } = siteCopy
  return (
    <div style={{ maxWidth: '48rem' }}>
      <section className="app-card" style={{
        background: 'white',
        color: '#333',
        borderRadius: 12,
        boxShadow: '0 10px 40px rgba(0,0,0,0.12)',
        padding: '1.5rem 2rem',
        marginBottom: '1.5rem',
      }}>
        <h2 className="app-card-title" style={{
          fontSize: '1.25rem',
          fontWeight: 700,
          marginBottom: '1rem',
          paddingBottom: '0.5rem',
          borderBottom: '2px solid #c41230',
        }}>
          <EditableText path="home.introTitle" />
        </h2>
        <p style={{ color: '#444', lineHeight: 1.7, marginBottom: '1rem' }}>
          <EditableText path="home.introPara1" />
        </p>
        <p style={{ color: '#444', lineHeight: 1.7, marginBottom: '1rem' }}>
          <EditableText path="home.introPara2" />
        </p>
        <p style={{ color: '#444', lineHeight: 1.7 }}>
          <EditableText path="home.introPara3" />
        </p>
      </section>

      <section className="app-card" style={{
        background: 'white',
        color: '#333',
        borderRadius: 12,
        boxShadow: '0 10px 40px rgba(0,0,0,0.12)',
        padding: '1.5rem 2rem',
        marginBottom: '1.5rem',
      }}>
        <h2 className="app-card-title" style={{
          fontSize: '1.25rem',
          fontWeight: 700,
          marginBottom: '1rem',
          paddingBottom: '0.5rem',
          borderBottom: '2px solid #c41230',
        }}>
          <EditableText path="home.studentTitle" />
        </h2>
        <p style={{ fontSize: '1.125rem', fontWeight: 600, color: '#c41230' }}>
          <EditableText path="project.student.name" />
        </p>
      </section>

      <section className="app-card" style={{
        background: 'white',
        color: '#333',
        borderRadius: 12,
        boxShadow: '0 10px 40px rgba(0,0,0,0.12)',
        padding: '1.5rem 2rem',
      }}>
        <h2 className="app-card-title" style={{
          fontSize: '1.25rem',
          fontWeight: 700,
          marginBottom: '1rem',
          paddingBottom: '0.5rem',
          borderBottom: '2px solid #c41230',
        }}>
          <EditableText path="home.supervisorsTitle" />
        </h2>
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {project.supervisors.map((_, i) => (
            <li key={i} style={{ marginBottom: '1rem' }}>
              <EditableText path={`project.supervisors.${i}.name`} style={{ fontWeight: 600, color: '#c41230' }} />
              <EditableText path={`project.supervisors.${i}.role`} style={{ display: 'block', fontSize: '0.875rem', color: '#666' }} />
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
