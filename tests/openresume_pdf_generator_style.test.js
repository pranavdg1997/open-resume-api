const assert = require('assert');

const {
  buildOpenResumeData,
  buildResumeLayoutModel,
} = require('../openresume_pdf_generator');

const resume = {
  personalInfo: {
    name: 'Pranav Gujarathi',
    email: 'pranav@example.com',
    phone: '+1 331 248 7381',
    location: 'Austin, TX',
    url: 'https://pranav.example.com',
    github: 'https://github.com/pranav',
    linkedin: 'https://linkedin.com/in/pranav',
    summary: 'AI engineer building production systems.',
  },
  workExperiences: [
    {
      company: 'Twin Health',
      jobTitle: 'Senior AI Engineer',
      date: 'January 2026 - Present',
      location: 'Remote',
      descriptions: ['Built agentic health workflows.'],
    },
  ],
  educations: [
    {
      school: 'Indiana University - Bloomington',
      degree: 'MS, Data Science',
      date: 'August 2019 - May 2021',
      descriptions: [],
    },
  ],
  skills: [
    { category: 'Skills', skills: ['Python', 'LLMs'] },
  ],
  settings: {
    fontSize: '11',
    documentSize: 'Letter',
  },
};

const data = buildOpenResumeData(resume);
const model = buildResumeLayoutModel(data);

assert.strictEqual(model.pageSize, 'A4');
assert.strictEqual(model.styles.page.fontFamily, 'Times-Roman');
assert.strictEqual(model.styles.page.color, '#000000');
assert.strictEqual(model.styles.sectionTitle.color, '#000000');
assert.strictEqual(model.styles.sectionTitle.borderBottomColor, '#000000');
assert.ok(model.styles.name.marginBottom >= 11);

assert.strictEqual(model.profile.name, 'PRANAV GUJARATHI');
assert.deepStrictEqual(model.profile.contactLines, [
  'pranav@example.com | +1 331 248 7381 | Austin, TX | https://pranav.example.com | https://github.com/pranav',
  'https://linkedin.com/in/pranav',
]);

assert.deepStrictEqual(model.sectionHeadings.slice(0, 4), [
  'PROFESSIONAL SUMMARY',
  'EDUCATION',
  'PROFESSIONAL EXPERIENCE',
  'SKILLS',
]);

assert.deepStrictEqual(model.workExperienceItems[0].headerRows, [
  { left: 'Twin Health', right: 'January 2026 - Present', emphasis: 'bold' },
  { left: 'Senior AI Engineer', right: 'Remote', emphasis: 'italic' },
]);

assert.deepStrictEqual(model.educationItems[0].headerRows, [
  { left: 'Indiana University - Bloomington', right: 'August 2019 - May 2021', emphasis: 'bold' },
  { left: 'MS, Data Science', right: '', emphasis: 'italic' },
]);

assert.ok(model.styles.bullet.marginLeft >= 18);
console.log('primary renderer ATS A4 component style model passed');
