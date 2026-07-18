const assert = require('assert');
const fs = require('fs');
const path = require('path');

const { generateOpenResumePDF } = require('../openresume_pdf_generator');

const resume = {
  personalInfo: {
    name: 'Publication Link Test',
    email: 'link@example.com',
    phone: '+1 555 111 2222',
    location: 'Austin, TX',
    url: 'https://portfolio.example.com',
    summary: 'AI engineer building production systems.',
  },
  workExperiences: [
    {
      company: 'Twin Health',
      jobTitle: 'Senior AI Engineer',
      date: 'January 2026 - Present',
      location: 'Remote',
      descriptions: ['Built production agent workflows.'],
    },
  ],
  publications: [
    {
      name: 'A Very Long Publication Title That Needs To Wrap Without Overlapping Metadata',
      date: 'ACM COMPASS 2026',
      url: 'https://example.com/paper',
      descriptions: ['Best paper finalist.'],
    },
  ],
  settings: {
    fontSize: '11',
    documentSize: 'Letter',
  },
};

(async () => {
  const pdf = await generateOpenResumePDF(resume);
  const outputPath = path.join(__dirname, '..', 'temp', 'primary-renderer-a4-smoke.pdf');
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, pdf);

  const pdfText = pdf.toString('latin1');
  assert.match(pdfText, /\/MediaBox\s+\[0 0 595\.280029 841\.890015\]/);
  assert.match(pdfText, /\/URI \(https:\/\/example\.com\/paper\)/);
  console.log('primary renderer PDF smoke passed');
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
