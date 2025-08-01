const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

const playerRoles = [
  'Batsman',
  'Bowler',
  'All-Rounder',
  'Wicket Keeper',
  'Opening Batsman',
  'Middle Order Batsman',
  'Fast Bowler',
  'Medium Pace Bowler',
  'Off Spin Bowler',
  'Leg Spin Bowler',
  'Left Arm Fast Bowler',
  'Right Arm Fast Bowler',
  'Left Arm Spinner',
  'Right Arm Spinner',
  'Captain',
  'Vice Captain',
  'Wicket Keeper Batsman',
  'Finisher',
  'Night Watchman',
  'Powerplay Specialist',
  'Death Over Specialist',
  'Strike Bowler',
  'Pinch Hitter',
  'Part-time Bowler'
];

async function seedPlayerRoles() {
  try {
    console.log('Starting player roles seeding...');

    for (const roleName of playerRoles) {
      // Check if role already exists
      const existingRole = await prisma.playerRole.findUnique({
        where: { name: roleName }
      });

      if (!existingRole) {
        await prisma.playerRole.create({
          data: {
            name: roleName,
            description: `Cricket player role: ${roleName}`,
            sportType: 'cricket',
            isActive: true
          }
        });
        console.log(`✅ Created player role: ${roleName}`);
      } else {
        console.log(`⏭️  Player role already exists: ${roleName}`);
      }
    }

    console.log('✅ Player roles seeding completed successfully!');
  } catch (error) {
    console.error('❌ Error seeding player roles:', error);
    throw error;
  } finally {
    await prisma.$disconnect();
  }
}

// Run the seeder if this file is executed directly
if (require.main === module) {
  seedPlayerRoles()
    .then(() => {
      console.log('Player roles seeder finished');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Player roles seeder failed:', error);
      process.exit(1);
    });
}

module.exports = { seedPlayerRoles }; 