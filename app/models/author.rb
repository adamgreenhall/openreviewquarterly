class Author < ActiveRecord::Base
  attr_accessible :first_name, :last_name, :biography, :image_url, :is_published, :is_publisher
  validates_presence_of :first_name, :last_name
  has_many :pieces
  has_many :illustrations
  scope :published_ordered, where(is_published: true).order('is_publisher desc, last_name, first_name')

  def name
    self.first_name+' '+self.last_name
  end
  def url
    '/people/'+URLify.urlify(self.name,'-')
  end
end
